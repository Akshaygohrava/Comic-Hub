from django.shortcuts import render, redirect
from .models import Product, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def hlogin(request):
    if request.method == "POST":
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginuserpassword"]

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, " Sucessfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            # return redirect('/')
    return render(request, "login.html")


def hlogout(request):
    # if request.method == 'POST':
    logout(request)

    return redirect("home")


def register(request):
    if request.method == "POST":
        username = request.POST.get("userid")
        fname = request.POST.get("username")
        lname = request.POST.get("userlastname")
        email = request.POST.get("useremail")
        password = request.POST.get("userpassword")
        cpassword = request.POST.get("usercpassword")

        if not username:
            messages.error(request, " Username Required")
        elif len(username) < 4:
            messages.error(request, " Username must be under characters")
        elif User.objects.filter(username=username).exists():
            messages.error(request, " Already User exist. Try Another username")
        elif not fname:
            messages.error(request, " First Name Required !!")
        elif len(fname) < 3 or len(fname) > 10:
            messages.error(request, " First Name must be 4 char long or more")
        elif not lname:
            messages.error(request, " Last Name Required..")
        elif len(lname) < 4 or len(lname) > 10:
            messages.error(request, " Last Name must be 4 char long or more")
        elif len(email) < 5 or len(email) < 16:
            messages.error(request, "Email must be 5 char long")
        elif User.objects.filter(email=email).exists():
            messages.error(request, " Email Already exist. Try Another Email")
        elif not password:
            messages.error(request, " Password Required")
        elif not cpassword:
            messages.error(request, " Confirm Password Required")
        elif len(password) < 6 or len(password) > 20:
            messages.error(request, " Password must be 6 char long")
        elif password != cpassword:
            messages.error(request, " Password do not match")

        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, " Account has been sucessfully created")
            return redirect("login")

    return render(request, "signup.html")


def home(request):
    if "cart" not in request.session:
        request.session["cart"] = []
    cart = request.session["cart"]
    request.session.set_expiry(0)
    ctx = {"cart": cart, "cart_size": len(cart)}
    return render(request, "store/home.html", ctx)


@login_required(login_url="login")
def storem(request):
    if "cart" not in request.session:
        request.session["cart"] = []
    cart = request.session["cart"]
    request.session.set_expiry(0)
    store_item = Product.objects.all()
    ctx = {"store_item": store_item, "cart_size": len(cart)}
    if request.method == "POST":
        cart.append(int(request.POST["obj_id"]))
        return redirect("storem")
    return render(request, "store/store.html", ctx)


def cartitem(cart):
    items = []
    for item in cart:
        items.append(Product.objects.get(id=item))
    return items


def genItemsList(cart):
    cart_item = cartitem(cart)
    items_list = ""
    for item in cart_item:
        items_list += str(item.name)
        items_list += ","
    return items_list


def totalcost(cart):
    cart_item = cartitem(cart)
    price = 0
    for item in cart_item:
        price += item.price
    return price


def cartview(request):
    cart = request.session["cart"]
    request.session.set_expiry(0)
    ctx = {
        "cart": cart,
        "cart_size": len(cart),
        "cart_item": cartitem(cart),
        "total": totalcost(cart),
    }
    return render(request, "store/cart.html", ctx)


def removefromcart(request):
    request.session.set_expiry(0)
    obj_remove = int(request.POST["obj_id"])
    obj_index = request.session["cart"].index(obj_remove)
    request.session["cart"].pop(obj_index)
    return redirect("cartview")


# Modify the checkout view
def checkout(request):
    request.session.set_expiry(0)
    cart = request.session["cart"]
    ctx = {"cart": cart, "cart_size": len(cart), "total": totalcost(cart)}
    return render(request, "store/checkout.html", ctx)

# Modify the completeorder view
def completeorder(request):
    request.session.set_expiry(0)
    cart = request.session["cart"]
    order = Order()
    order.name = request.POST["name"]
    order.address = request.POST["address"]
    order.phone = request.POST["phone"]
    order.payment_method = request.POST["payment"]
    order.payment_data = request.POST["payment_data"]
    order.item = genItemsList(cart)
    order.total_price = totalcost(cart)  # Add this line to store the total price in the Order model
    order.save()
    request.session["cart"] = []
    return render(request, "store/complete.html", {"total": totalcost(cart)})  # Include the total in the context



def about(request):
    request.session.set_expiry(0)
    cart = request.session["cart"]
    ctx = {"cart": cart, "cart_size": len(cart)}
    return render(request, "store/about.html", ctx)


from django.shortcuts import render
from .models import Order  # Replace with your actual Order model


def orders(request):
    # Retrieve orders from the database or session, and pass them to the template
    orders = Order.objects.all()  # Fetch orders using your model
    context = {"receipts": orders}
    return render(request, "store/orders.html", context)


from .models import Order


def order_history(request):
    orders = Order.objects.all().order_by("-timestamp")
    return render(request, "store/orders.html", {"orders": orders})
