
import grpc
from uuid import UUID

import app.api.gRPC_api_helpers.auth_pb2 as pb2
import app.api.gRPC_api_helpers.auth_pb2_grpc as pb2_grpc

from app.core.config import settings
from app.utils.logger import logger


channel = grpc.insecure_channel(
    settings.AUTH_HOST
)

stub = pb2_grpc.AuthServiceStub(
    channel
)


class AuthClient:

    def get_email_by_id(
        self,
        user_id: UUID
    ) -> str | None:

        try:

            response = stub.GetEmail(
                pb2.UserRequest(
                    user_id=str(user_id)
                )
            )

            return response.email

        except grpc.RpcError as ex:

            logger.error(
                f"Failed to get email for {user_id}: {ex}"
            )

            return None

    def get_phone_by_id(
        self,
        user_id: UUID
    ) -> str | None:

        try:

            response = stub.GetPhone(
                pb2.UserRequest(
                    user_id=str(user_id)
                )
            )

            return response.phone

        except grpc.RpcError as ex:

            logger.error(
                f"Failed to get phone for {user_id}: {ex}"
            )

            return None
        
    def is_admin(self)-> bool:
        try:
            (...)
            return True
        except grpc.RpcError as ex:
            logger.exception(f"Failed to check admin or not")
            return False


auth_client = AuthClient()
