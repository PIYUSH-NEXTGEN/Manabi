from datetime import timedelta

from fastapi import APIRouter

from app import schemas
from app.deps import DB, CurrentUser
from app.models import User, as_utc, utcnow
from app.services import github
from app.services.presenters import problem_to_out
from app.services.recommender import recommendations_for_user

router = APIRouter(tags=["recommendations"])

SIGNALS_TTL = timedelta(minutes=10)


async def _refresh_signals(db: DB, user: User) -> None:
    fresh = user.signals_updated_at is not None and (utcnow() - as_utc(user.signals_updated_at)) < SIGNALS_TTL
    if user.signals_json is not None and fresh:
        return
    signals = await github.get_user_signals(user.github_token)
    if signals is not None:
        user.signals_json = signals
        user.signals_updated_at = utcnow()
        db.commit()


@router.get("/api/recommendations", response_model=schemas.RecommendationsOut)
async def recommendations(user: CurrentUser, db: DB):
    await _refresh_signals(db, user)
    items = [
        schemas.RecommendationItem(
            problem=problem_to_out(problem, 0),
            score=score,
            reasons=reasons,
        )
        for problem, score, reasons in recommendations_for_user(db, user)
    ]
    return schemas.RecommendationsOut(items=items)
