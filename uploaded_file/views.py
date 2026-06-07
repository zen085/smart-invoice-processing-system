from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from .forms import UploadFileForm
from .tasks import process_uploaded_file_task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import UploadedFile
from django.http import JsonResponse
# Create your views here.

class UploadFileView(LoginRequiredMixin,CreateView):
    model = UploadedFile
    form_class = UploadFileForm
    template_name = "upload.html"
    success_url = reverse_lazy("upload-dashboard")
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.status = UploadedFile.UploadStatus.PENDING
        self.object.save()
       
        process_uploaded_file_task.delay(self.object.id)

        return render(self.request,"upload_processing.html",{"file":self.object})

    

class UploadDashboardView(LoginRequiredMixin,ListView):
    model = UploadedFile
    template_name = "dashboard.html"
    context_object_name = "uploaded_files"
    ordering = ["-created_at"]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user,is_hidden=False).order_by("-created_at")

class UploadStatusView(View):
    def get(self,request,pk):
        file = get_object_or_404(UploadedFile,pk=pk)
        return JsonResponse(
            {
                "status":file.status.lower(),
                "error": file.error_message.lower()
            }
        )

class ClearDashboardView(LoginRequiredMixin,View):
    def post(self,request,*arg,**kwargs):
        UploadedFile.objects.filter(user=request.user).update(is_hidden=True)
        return redirect("upload-dashboard")


