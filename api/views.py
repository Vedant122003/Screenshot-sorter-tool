import subprocess
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)  # Corrected the logger initialization

@csrf_exempt
def upload_images(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        clusters = request.POST.get('clusters', 5)  # Default to 5 if not provided
        try:
            clusters = int(clusters)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid number of clusters'}, status=400)

        fs = FileSystemStorage(location=settings.IMAGES_STORE)
        saved_files = []

        for image in images:
            filename = fs.save(image.name, image)
            saved_files.append(os.path.join(settings.IMAGES_STORE, filename))
            logger.debug(f"Saved file: {filename}")

        # Run clustering script after saving images
        cluster_script_path = os.path.join(settings.BASE_DIR, 'OPENAI-CLIP-COPY', 'sample1.py')
        images_folder = settings.IMAGES_STORE
        clusters_folder = os.path.join(settings.BASE_DIR, 'clusters')

        process = subprocess.Popen(['python', cluster_script_path, images_folder, clusters_folder, str(clusters)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        logger.debug(f"Clustering script stdout: {stdout.decode('utf-8')}")
        logger.error(f"Clustering script stderr: {stderr.decode('utf-8')}")

        if process.returncode == 0:
            logger.debug("Clustering script executed successfully")
            return JsonResponse({'status': 'success', 'message': 'Clustering script executed successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': f'Error running clustering script: {stderr.decode("utf-8")}'}, status=500)

    return JsonResponse({'status': 'failure'}, status=400)
