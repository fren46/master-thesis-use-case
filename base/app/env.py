from dependency_injector import providers as providers
from krules_core.providers import (
    subject_storage_factory,
    configs_factory
)
from k8s_subjects_storage import storage_impl as k8s_storage_impl
import os

def init():
    # This is an inmemory database and it is not persistent
    # you probably want to comment out this configuration and enable a more appropriate one

    # from krules_core.tests.subject.sqlite_storage import SQLLiteSubjectStorage
    # subject_storage_factory.override(
    #    providers.Factory(lambda x: SQLLiteSubjectStorage(x, ":memory:"))
    # )

    #Redis subjects storage support
    subjects_redis_storage_settings = configs_factory() \
        .get("subjects-backends") \
        .get("redis")
    from redis_subjects_storage import storage_impl as redis_storage_impl

    subject_storage_factory.override(
        providers.Factory(lambda name, event_info, event_data:
                  name.startswith("k8s:") and k8s_storage_impl.SubjectsK8sStorage(
                      resource_path=name[4:],
                      resource_body=event_data
                  )
                  or redis_storage_impl.SubjectsRedisStorage(name, subjects_redis_storage_settings.get("url"))
        )
    )


    # MongoDB subjects storage support
    # subjects_mongodb_storage_settings = configs_factory() \
    #     .get("subjects-backends") \
    #     .get("mongodb")
    #
    # from mongodb_subjects_storage import storage_impl as mongo_storage_impl
    #
    # client_args = subjects_mongodb_storage_settings["client_args"]
    # client_kwargs = subjects_mongodb_storage_settings["client_kwargs"]
    # database = subjects_mongodb_storage_settings["database"]
    # collection = subjects_mongodb_storage_settings.get("collection", "subjects")
    # use_atomic_ops_collection = subjects_mongodb_storage_settings.get("use_atomic_ops_collection", False)
    # atomic_ops_collection_size = subjects_mongodb_storage_settings.get("atomic_ops_collection_size", 5242880)
    # atomic_ops_collection_max = subjects_mongodb_storage_settings.get("atomic_ops_collection_max", 1000)
    #
    # subject_storage_factory.override(
    #     providers.Factory(
    #         lambda x: mongo_storage_impl.SubjectsMongoStorage(x, database, collection,
    #                                                           client_args=client_args, client_kwargs=client_kwargs,
    #                                                           use_atomic_ops_collection=use_atomic_ops_collection,
    #                                                           atomic_ops_collection_size=atomic_ops_collection_size,
    #                                                           atomic_ops_collection_max=atomic_ops_collection_max
    #                                                           ))
    #)
