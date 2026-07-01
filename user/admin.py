from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Deposit, Bonus, ReferalBonus, Withdrawal, UserInvestment, UserAccount, ReferalList,Profit,Penalty,KYCVerification,Otp,WithdrawalInfo

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Unregister the original User admin, then register the new one
admin.site.unregister(User)





@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'coin', 'date', 'status')
    list_filter = ('status', 'coin', 'date')
    search_fields = ('user__username', 'coin')
    date_hierarchy = 'date'

@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'type', 'date')
    list_filter = ('type', 'date')
    search_fields = ('user__username',)

@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'type', 'date')
    list_filter = ('type', 'date')
    search_fields = ('user__username',)

@admin.register(ReferalBonus)
class ReferalBonusAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'type', 'date')
    list_filter = ('type', 'date')
    search_fields = ('user__username',)

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'type' ,'status', 'date')
    list_filter = ('type',)
    search_fields = ('user__username',)

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'account_balance', 'total_profit',
        'bonus', 'referal_bonus', 'total_deposit', 'total_withdrawal'
    )
    search_fields = ('user__username',)
    list_filter = ('account_balance',)

@admin.register(ReferalList)
class ReferalListAdmin(admin.ModelAdmin):
    list_display=(
        'client_name', 'ref_level', "client_status", "date_registered"
    )

@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'type', 'start_date', 'end_date', 'profit_earned', 'is_active', 'matured')


@admin.register(Profit)
class ProfitAdmin(admin.ModelAdmin):
    list_display=(
        'user', 'plan', 'amount','type', 'date'
    )



@admin.register(KYCVerification)
class KYCAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'date_of_birth',
        'nationality',
        'is_approved',
        'submitted_at'
    )
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('is_approved', 'nationality', 'submitted_at')
    readonly_fields = ('submitted_at',)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'otp'
    )


@admin.register(WithdrawalInfo)
class WithdrawalInfoAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'bank_name',
        'account_name',
        'account_number',
        'swift_code',
        'bitcoin_address',
        'ethereum_address',
        'litecoin_address',
        'usdt_trc20_address',
    )




from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import BroadcastEmailForm
from .utils import send_admin_broadcast_email

User = get_user_model()


class UserAdmin(admin.ModelAdmin):  # keep your existing UserAdmin config, just add the parts below
    change_list_template = "admin/user/user_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-broadcast-email/",
                self.admin_site.admin_view(self.send_broadcast_email),
                name="send_broadcast_email",
            ),
        ]
        return custom_urls + urls

    def send_broadcast_email(self, request):
        if request.method == "POST":
            form = BroadcastEmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data["subject"]
                message = form.cleaned_data["message"]
                send_to_all = form.cleaned_data["send_to_all"]

                recipients = User.objects.all() if send_to_all else form.cleaned_data["users"]

                sent = 0
                for user in recipients:
                    if user.email:
                        if send_admin_broadcast_email(user, subject, message):
                            sent += 1

                messages.success(request, f"Email sent to {sent} user(s).")
                return redirect("..")
        else:
            form = BroadcastEmailForm()

        return render(request, "admin/send_broadcast_email.html", {"form": form})


admin.site.register(User, UserAdmin)