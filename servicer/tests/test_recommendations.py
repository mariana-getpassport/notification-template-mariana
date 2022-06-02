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

from .test_base import PackageTestBase
from package_server.recommendations import books_by_category


class TestRecommendAPI(PackageTestBase):
    """Test Handler for Recommend API definition."""

    def _recommend(self, request: RecommendationRequest) -> None:
        """
        Test the recommend end point.

        Returns: None
        """
        with grpc.insecure_channel(f"{self.server.host}:{self.server.port}") as channel:
            client = RecommendationsStub(channel)
            response: RecommendationResponse = client.Recommend(request)
            self.assertEqual(type(response).__name__, "RecommendationResponse")
            self.assertEqual(len(response.recommendations), request.max_results)
            check_response: BookRecommendation = response.recommendations[0]
            self.assertTrue(
                check_response in cast(list[BookRecommendation], books_by_category.get(BookCategory.SCIENCE_FICTION))
            )

    def test_recommend_success(self) -> None:
        """
        Test the recommend end point.

        Returns: None
        """
        request_one: RecommendationRequest = RecommendationRequest(
            user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=1
        )

        self._recommend(request_one)

        request_three: RecommendationRequest = RecommendationRequest(
            user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3
        )

        self._recommend(request_three)

    def test_recommend_fail(self) -> None:
        """
        Test the recommend end point with bad data.

        Returns: None
        """
        request: RecommendationRequest = RecommendationRequest(user_id=1, category=99, max_results=1)

        with grpc.insecure_channel(f"{self.server.host}:{self.server.port}") as channel:
            client = RecommendationsStub(channel)
            with pytest.raises(grpc.RpcError) as exception_info:
                response: RecommendationResponse = client.Recommend(request)
                self.assertEqual(len(response.recommendations), 0)
            assert exception_info.value.code() == grpc.StatusCode.NOT_FOUND
