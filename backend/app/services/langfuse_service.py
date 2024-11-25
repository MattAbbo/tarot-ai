# app/services/langfuse_service.py
from langfuse import Langfuse
import os
from typing import Dict, Any, Optional
import asyncio
from functools import partial

class LangfuseService:
    def __init__(self):
        print("Initializing LangfuseService...")
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY")
        )
        print("LangfuseService initialized successfully")
    
    async def _run_sync(self, func, *args, **kwargs):
        """Helper method to run synchronous Langfuse operations in async context"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))
    
    async def track_reading(self, session_id: str, reading_data: Dict[str, Any]) -> None:
        print(f"\n--- Starting track_reading for session {session_id} ---")
        try:
            print("Creating trace...")
            # Create trace synchronously since it's needed for subsequent operations
            trace = self.langfuse.trace(
                id=session_id,
                name="tarot_reading"
            )

            # Run generation span creation asynchronously
            print("Creating generation span...")
            await self._run_sync(
                trace.generation,
                name="card_interpretation",
                model=reading_data["model"],
                model_parameters={"max_tokens": 400},
                prompt=[
                    {
                        "role": "system",
                        "content": reading_data["system_prompt"]
                    },
                    {
                        "role": "user",
                        "content": reading_data["user_prompt"]
                    }
                ],
                completion=reading_data["completion"]
            )

            # Run metadata span creation asynchronously
            print("Creating metadata span...")
            await self._run_sync(
                trace.span,
                name="reading_metadata",
                input={
                    "card_name": reading_data["card_name"],
                    "original_question": reading_data.get("context"),
                    "has_reflection": bool(reading_data.get("reflection"))
                }
            )

            print("Track reading completed successfully")

        except Exception as e:
            print(f"Error in track_reading: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            # Don't re-raise the exception - we want to log errors but not fail the main flow

    async def track_image_interpretation(self, session_id: str, interpretation_data: Dict[str, Any]) -> None:
        print(f"\n--- Starting track_image_interpretation for session {session_id} ---")
        try:
            print("Creating trace...")
            trace = self.langfuse.trace(
                id=session_id,
                name="image_interpretation"
            )

            print("Creating generation span...")
            await self._run_sync(
                trace.generation,
                name="image_analysis",
                model=interpretation_data["model"],
                model_parameters={"max_tokens": 400},
                prompt=[
                    {
                        "role": "system",
                        "content": interpretation_data["system_prompt"]
                    }
                ],
                completion=interpretation_data["completion"]
            )

            print("Track image interpretation completed successfully")

        except Exception as e:
            print(f"Error in track_image_interpretation: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    async def track_error(self, session_id: str, error: str, context: str) -> None:
        print(f"\n--- Starting track_error for session {session_id} ---")
        try:
            print("Creating trace...")
            trace = self.langfuse.trace(
                id=session_id,
                name=f"error_{context}"
            )

            print("Creating error span...")
            await self._run_sync(
                trace.span,
                name="error",
                input={
                    "error_message": error,
                    "context": context
                }
            )

            print("Track error completed successfully")

        except Exception as e:
            print(f"Error in track_error: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    async def score_reading(self, session_id: str, score: float, feedback: Optional[str] = None) -> None:
        print(f"\n--- Starting score_reading for session {session_id} ---")
        try:
            print("Submitting score...")
            await self._run_sync(
                self.langfuse.score,
                name="user_satisfaction",
                trace_id=session_id,
                value=score,
                comment=feedback
            )
            print("Score submitted successfully")

        except Exception as e:
            print(f"Error in score_reading: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

# Create singleton instance
langfuse_service = LangfuseService()