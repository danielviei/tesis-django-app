from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from project.apps.publication.models import Publication
from project.apps.comments.serializers import CommentSerializer


class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            publication = Publication.objects.get(pk=pk)
            serializer.save(author_id=request.user, publication_id=publication)
            # Replace with your logic for generating comments HTML
            comments_html = self.get_context_data(pk)["comments_html"]
            return Response({"comments_html": comments_html})
        else:
            return Response(serializer.errors, status=400)

    def get_context_data(self, pk):
        publication = Publication.objects.get(pk=pk)
        comments = publication.comments.all()

        # Replace this with your template logic for rendering comments
        comments_html = '<ul class="list-none space-y-4">'
        for comment in comments:
            comments_html += f"""
            <li class="p-4 rounded-md bg-gray-100">
                <div class="flex items-center">
                    <img src="{comment.author_id.img.url}" alt="{comment.author_id.email} profile picture" class="w-10 h-10 rounded-full mr-4">
                    <div>
                        <h4 class="text-md font-bold text-gray-800">{comment.author_id.email}</h4>
                        <p class="text-gray-600">{comment.content}</p>
                    </div>
                </div>
            </li>
            """
        comments_html += "</ul>"

        return {"comments_html": comments_html}
