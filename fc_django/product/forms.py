from django import forms
from django.contrib.auth.hashers import check_password, make_password
from .models import Product

class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': '상품명을 입력해주세요.'
        },
        max_length=65, label='상품명'
    )
    price = forms.IntegerField(
        error_messages={
            'required': '상품가격을 입력해주세요.'
        },
        label='상품가격'
    )
    description = forms.CharField(label='상품설명')
    stuck = forms.IntegerField(
        error_messages={
            'required': '재고를 입력해주세요.'
        },
        label='재고'
    )
    
    def clean(self):
        clened_data = super().clean()
        name = clened_data.get('name')
        price = clened_data.get('price')
        description = clened_data.get('description')
        stuck = clened_data.get('stuck')


        if name and price and description and stuck:
            product = Product(
                name=name,
                price=price,
                description=description,
                stuck=stuck,
            )
                
            product.save()


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )

    def clean(self):
        clened_data = super().clean()
        email = clened_data.get('email')
        password = clened_data.get('password')

        if email and password:
            try:
                fcuser = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:
                self.add_error('email', '등록된 이메일이 없습니다')
                return
                
            if not check_password(password, fcuser.password):
                self.add_error('password', '비밀번호를 틀렸습니다.')
            else:
                self.email = fcuser.email