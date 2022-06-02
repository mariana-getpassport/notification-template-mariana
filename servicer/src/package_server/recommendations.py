"""Recommendations.py."""

import logging
import random

import grpc
from package_grpc.v1.recommendations_pb2 import (  # pylint: disable=C0411
    BookCategory,
    BookRecommendation,
    RecommendationRequest,
    RecommendationResponse,
)
from package_grpc.v1.recommendations_pb2_grpc import RecommendationsServicer  # pylint: disable=C0411

# Module logger.
_log = logging.getLogger(__name__)

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=4, title="The Hitchhiker's Guide to the Galaxy"),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=7, title="The 7 Habits of Highly Effective People"),
        BookRecommendation(id=8, title="How to Win Friends and Influence People"),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
    ],
}


class RecommendationService(RecommendationsServicer):
    """RecommendationService Class.

    :recommendations_pb2_grpc.RecommendationsServicer: servicer function which is passed.
    """

    def Recommend(  # noqa: N802
        self, request: RecommendationRequest, context: grpc.ServicerContext
    ) -> RecommendationResponse:  # pylint: disable=unused-argument,R0201
        """Entry point for the RecommendationService.

        :request: requested type of book category
        :context: servicer context for returning errors
        """
        if request.category not in books_by_category:
            _log.error("Category not found: %s", request.category)
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)

        _log.info("%s results found", len(books_to_recommend))
        return RecommendationResponse(recommendations=books_to_recommend)
