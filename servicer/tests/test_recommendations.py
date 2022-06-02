"""Test the customers module."""
# isort: skip_file

from typing import cast
import grpc
import pytest

import sqlalchemy
from orm.session import DBSession

import package_grpc.v1.recommendations_pb2 as rec_pb2
import package_grpc.v1.recommendations_pb2_grpc as rec_pb2_grpc

from package_server import model


def recommend(config, request: rec_pb2.RecommendationRequest) -> None:
    """Test the recommend end point."""
    host = config.get("grpc", "server.host")
    port = config.getint("grpc", "server.port")
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        client = rec_pb2_grpc.RecommendationsStub(channel)
        response: rec_pb2.RecommendationResponse = client.Recommend(request)
        assert type(response).__name__ == "RecommendationResponse"
        assert len(response.recommendations) == request.max_results
        check_response: rec_pb2.BookRecommendation = response.recommendations[0]
        with DBSession() as session, session.begin():
            book = cast(
                model.Book,
                session.execute(sqlalchemy.select(model.Book).where(model.Book.title == check_response.title)).scalar(),
            )
            assert book.category_id == request.category


def test_recommend_success(config, server) -> None:  # pylint: disable=unused-argument
    """Test the recommend end point."""
    request_one: rec_pb2.RecommendationRequest = rec_pb2.RecommendationRequest(
        user_id=1, category=rec_pb2.BookCategory.SCIENCE_FICTION, max_results=1
    )

    recommend(config, request_one)

    request_three: rec_pb2.RecommendationRequest = rec_pb2.RecommendationRequest(
        user_id=1, category=rec_pb2.BookCategory.SCIENCE_FICTION, max_results=3
    )

    recommend(config, request_three)


def test_recommend_fail(config, server) -> None:  # pylint: disable=unused-argument
    """Test the recommend end point with bad data."""
    request: rec_pb2.RecommendationRequest = rec_pb2.RecommendationRequest(user_id=1, category=99, max_results=1)

    host = config.get("grpc", "server.host")
    port = config.getint("grpc", "server.port")
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        client = rec_pb2_grpc.RecommendationsStub(channel)
        with pytest.raises(grpc.RpcError) as exception_info:
            response: rec_pb2.RecommendationResponse = client.Recommend(request)
            assert len(response.recommendations) == 0
        assert exception_info.value.code() == grpc.StatusCode.NOT_FOUND
