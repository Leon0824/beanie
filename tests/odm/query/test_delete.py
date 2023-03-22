from tests.odm.models import Sample
from beanie.odm.queries.delete import DeleteMany


async def test_delete_many(preset_documents):
    count_before = await Sample.count()
    count_find = (
        await Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .count()
    )
    await Sample.find_many(Sample.integer > 1).find_many(
        Sample.nested.optional is None
    ).delete()
    count_after = await Sample.count()
    assert count_before - count_find == count_after

    assert isinstance(
        Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .delete_many(),
        DeleteMany,
    )


async def test_delete_all(preset_documents):
    await Sample.delete_all()
    count_after = await Sample.count()
    assert count_after == 0


async def test_delete_self(preset_documents):
    count_before = await Sample.count()
    result = (
        await Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .to_list()
    )
    a = result[0]
    await a.delete()
    count_after = await Sample.count()
    assert count_before == count_after + 1


async def test_delete_one(preset_documents):
    count_before = await Sample.count()
    await Sample.find_one(Sample.integer > 1).find_one(
        Sample.nested.optional is None
    ).delete()
    count_after = await Sample.count()
    assert count_before == count_after + 1

    count_before = await Sample.count()
    await Sample.find_one(Sample.integer > 1).find_one(
        Sample.nested.optional is None
    ).delete_one()
    count_after = await Sample.count()
    assert count_before == count_after + 1


async def test_delete_many_with_session(preset_documents, session):
    count_before = await Sample.count()
    count_find = (
        await Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .count()
    )
    q = (
        Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .delete(session=session)
    )
    assert q.session == session

    q = (
        Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .delete()
        .set_session(session=session)
    )

    assert q.session == session

    await q

    count_after = await Sample.count()
    assert count_before - count_find == count_after
