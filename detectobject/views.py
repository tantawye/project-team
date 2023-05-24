from django.shortcuts import render
from subprocess import Popen, PIPE
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64, json
import os
@csrf_exempt
def ObjectDetectionView(request):
    if request.method == 'POST':
        default_camera = int(request.POST.get('defaultCameraIndex').strip("'"))
        command = f'python detect.py --source {default_camera}'
        cwd1 = os.path.join(os.getcwd(), 'detectobject', 'yolov7')

        # Run the command to perform object detection
        process = Popen(command, shell=True, cwd=cwd1, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        def stream_output():
            for line in process.stdout:
                line = line.strip()
                if line.startswith('seem'):
                    s = line[len('seem'):].strip()
                elif line.startswith('byte'):
                    base64_str = line[len('byte'):].strip()
                    yield f"data: {json.dumps({'object_name': s, 'base64_str': base64_str})}\n\n"

        return StreamingHttpResponse(stream_output(), content_type='text/event-stream')

    elif request.method == 'GET':
        default_camera = request.GET.get('source', '0')
        command = f'python detect.py --source {default_camera}'
        cwd1 = os.path.join(os.getcwd(), 'detectobject', 'yolov7')

        # Run the command to perform object detection
        process = Popen(command, shell=True, cwd=cwd1, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        def stream_output():
            for line in process.stdout:
                line = line.strip()
                if line.startswith('seem'):
                    s = line[len('seem'):].strip()
                elif line.startswith('byte'):
                    base64_str = line[len('byte'):].strip()
                    yield f"data: {json.dumps({'object_name': s, 'base64_str': base64_str})}\n\n"

        return StreamingHttpResponse(stream_output(), content_type='text/event-stream')

    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."})
