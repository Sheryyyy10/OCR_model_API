from django.core.files.storage import default_storage
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')


class OCRView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            if 'image' not in request.FILES:
                return Response({'status': 'error', 'message': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

            image = request.FILES['image']
            try:
                image_path = default_storage.save(f"temp/{image.name}", image)
                full_image_path = default_storage.path(image_path)
            except Exception as e:
                return Response({'status': 'error', 'message': 'Failed to save image', 'details': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                result = ocr.ocr(full_image_path, cls=True)
                # Clean up the temporary image file
                default_storage.delete(image_path)
            except Exception as e:
                return Response({'status': 'error', 'message': 'OCR processing failed', 'details': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            result_text = '\n'.join([' '.join([line[1][0] for line in res]) for res in result])

            return Response({'status': 'success', 'message': None, 'Data': result_text})

        except Exception as e:
            return Response({'status': 'error', 'message': 'An unexpected error occurred', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
