"""Test the customers module."""
# isort: skip_file

from typing import cast
import grpc
import pytest

from package_grpc.v1.recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationRequest,
    RecommendationResponse,
)  # pylint: disable=C0411
from package_grpc.v1.recommendations_pb2_grpc import RecommendationsStub  # pylint: disable=C0411

from package_server.recommendations import books_by_category


def recommend(config, request: RecommendationRequest) -> None:
    """Test the recommend end point."""
    host = config.get("grpc", "server.host")
    port = config.getint("grpc", "server.port")
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        client = RecommendationsStub(channel)
        response: RecommendationResponse = client.Recommend(request)
        assert type(response).__name__ == "RecommendationResponse"
        assert len(response.recommendations) == request.max_results
        check_response: BookRecommendation = response.recommendations[0]
        scifi_books = books_by_category.get(BookCategory.SCIENCE_FICTION)
        assert check_response in cast(list[BookRecommendation], scifi_books)


def test_recommend_success(config, server) -> None:  # pylint: disable=unused-argument
    """Test the recommend end point."""
    request_one: RecommendationRequest = RecommendationRequest(
        user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=1
    )

    recommend(config, request_one)

    request_three: RecommendationRequest = RecommendationRequest(
        user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3
    )

    recommend(config, request_three)


def test_recommend_fail(config, server) -> None:  # pylint: disable=unused-argument
    """Test the recommend end point with bad data."""
    request: RecommendationRequest = RecommendationRequest(user_id=1, category=99, max_results=1)

    host = config.get("grpc", "server.host")
    port = config.getint("grpc", "server.port")
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        client = RecommendationsStub(channel)
        with pytest.raises(grpc.RpcError) as exception_info:
            response: RecommendationResponse = client.Recommend(request)
            assert len(response.recommendations) == 0
        assert exception_info.value.code() == grpc.StatusCode.NOT_FOUND
