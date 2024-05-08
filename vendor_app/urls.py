from django.urls import path
from vendor_app.views import VendorListCreateAPIView, VendorDetailAPIView, PurchaseOrderListCreateAPIView, \
    PurchaseOrderDetailAPIView, HistoricalPerformanceListCreateAPIView, HistoricalPerformanceDetailAPIView

urlpatterns = [
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('purchase-orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('purchase-orders/<int:pk>/', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),
    path('historical-performances/', HistoricalPerformanceListCreateAPIView.as_view(), name='historical-performance-list-create'),
    path('historical-performances/<int:pk>/', HistoricalPerformanceDetailAPIView.as_view(), name='historical-performance-detail'),
]
