from django.contrib import admin
from .models import Product, Contact, Order, OrderItem
from django.core.mail import send_mail       # ← add this line
from django.conf import settings
# Register your models here
admin.site.register(Product)
admin.site.register(Contact)

# Inline for line‑items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('order_id', 'full_name', 'email', 'phone', 'date_ordered')
    inlines         = [OrderItemInline]
    readonly_fields = ('date_ordered',)

    actions = ['send_shipment_email']

    def send_shipment_email(self, request, queryset):
        for order in queryset:
            subject = f"Your Order #{order.order_id} Is On Its Way!"
            message = (
                f"Hi {order.full_name},\n\n"
                "Thanks for shopping with us! Your order is being processed and will arrive soon.\n\n"
                f"Track your order here: https://example.com/track/{order.order_id}\n\n"
                "If you have any questions, just reply to this email.\n\n"
                "Best,\nThe E‑Commerce Team"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=False,
            )
        # This should be *outside* the for‑loop
        self.message_user(request, f"Sent shipment emails for {queryset.count()} orders.")

    send_shipment_email.short_description = "Send shipment email to selected orders"

from django.contrib import admin
# from .models import Profile

# admin.site.register(Profile)
