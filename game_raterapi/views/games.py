"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from game_raterapi.models import Game, Category, Rater, Game_Category


class Games(ViewSet):
    """Game Rater Games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        rater = Rater.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        game = Game()
        game.rater = rater
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.estimated_time = request.data["estimatedTime"]
        game.age_recommended = request.data["ageRecommendation"]
        
        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        rater = Rater.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        game = Game.objects.get(pk=pk)
        game.rater = rater
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.estimated_time = request.data["estimatedTime"]
        game.age_recommended = request.data["ageRecommendation"]

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        games = Game.objects.all()
        categories = Category.objects.all()

        for game in games:
            game.categories = None

            try:
                Game_Category.objects.get(game=game, categories=categories)
                game.category = categories.label
            except Game_Category.DoesNotExist:
                game.category = None


        category = self.request.query_params.get('category', None)
        if category is not None:
            games = games.filter(category__id=category)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def category(self, request, pk=None):
        """Managing categories for games"""

        # A gamer wants to sign up for an game
        if request.method == "POST":
            # The pk would be `2` if the URL above was requested
            game = Game.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which user is making the request to sign up
            category = Category.objects.get(pk=pk)

            try:
                # Determine if the user is already signed up
                categorization = Game_Category.objects.get(
                    game=game, category=category)
                return Response(
                    {'message': 'Category is already assigned'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except Game_Category.DoesNotExist:
                # The user is not signed up.
                categorization = Game_Category()
                categorization.game = game
                categorization.category = category
                categorization.save()

                return Response({}, status=status.HTTP_201_CREATED)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'year_released', 'number_of_players', 'estimated_time', 'age_recommendation', 'category')
        depth = 1