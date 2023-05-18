from django.shortcuts import render
from subprocess import run , PIPE 

from django.http import JsonResponse ,StreamingHttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
import base64,  json



@csrf_exempt

def ObjectDetectionView(request):
        if request.method == 'POST':
            default_camera = int(request.POST.get('defaultCameraIndex').strip("'"))
            command = f'python detect.py --source {default_camera}'

            # Run the command to perform object detection
            result = run(command, shell=True, check=True, cwd=r'detectobject\yolov7', stdout=PIPE, stderr=PIPE)
            # Process the output to extract im0 and s
            output_lines = result.stdout.decode().split('\n')
            s = None
            base64_str = None
            for line in output_lines:
                if line.startswith('seem'):
                    s = line[len('seem'):].strip()
                if line.startswith('byte'):
                    base64_str = line[len('byte'):]

            response_data = {
                's': s,
                'base64_str': base64_str
            }
            return StreamingHttpResponse(json.dumps(response_data) + '\n', content_type='text/event-stream')
        
            # return JsonResponse(response_data, safe=False)
        
        elif request.method == 'GET':
            default_camera = request.GET.get('source', '0')
            command = f'python detect.py --source {default_camera}'

            # Run the command to perform object detection
            result = run(command, shell=True, check=True, cwd=r'detectobject\yolov7', stdout=PIPE, stderr=PIPE)

            # Process the output to extract im0 and s
            output_lines = result.stdout.decode().split('\n')
            s = None
            base64_str = None
            for line in output_lines:
                if line.startswith('seem'):
                    s = line[len('seem'):].strip()
                if line.startswith('byte'):
                    base64_str = line[len('byte'):]
          

            response_data = {
                's': s,
                'base64_str': base64_str
            }
            return StreamingHttpResponse(json.dumps(response_data) + '\n', content_type='text/event-stream')

        else:
            return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def api2(request):
    return ObjectDetectionView(request)


        