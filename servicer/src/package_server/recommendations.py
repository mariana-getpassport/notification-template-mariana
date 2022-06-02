"""Recommendations.py."""

import logging
import random

import grpc
import package_grpc.v1.recommendations_pb2 as rec_pb2
import package_grpc.v1.recommendations_pb2_grpc as rec_pb2_grpc
import sqlalchemy
from orm.session import DBSession
from package_server import model

# Module logger.
_log = logging.getLogger(__name__)


class RecommendationService(rec_pb2_grpc.RecommendationsServicer):
    """RecommendationService Class.

    :recommendations_pb2_grpc.RecommendationsServicer: servicer function which is passed.
    """

    def Recommend(  # noqa: N802
        self, request: rec_pb2.RecommendationRequest, context: grpc.ServicerContext
    ) -> rec_pb2.RecommendationResponse:  # pylint: disable=unused-argument,R0201
        """Entry point for the RecommendationService.

        :request: requested type of book category
        :context: servicer context for returning errors
        """
        with DBSession() as session, session.begin():
            category = session.execute(
                sqlalchemy.select(model.BookCategory).where(model.BookCategory.id == request.category)
            ).scalar()
            if category is None:
                _log.error("Category not found: %s", request.category)
                context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
            books_for_category = (
                session.execute(sqlalchemy.select(model.Book).where(model.Book.category_id == request.category))
                .scalars()
                .all()
            )

            num_results = min(request.max_results, len(books_for_category))
            recommendations = [
                rec_pb2.BookRecommendation(id=i + 1, title=book.title) for i, book in enumerate(books_for_category)
            ]
            recommendations = random.sample(recommendations, num_results)

            _log.info("%s results found", len(recommendations))
            return rec_pb2.RecommendationResponse(recommendations=recommendations)
