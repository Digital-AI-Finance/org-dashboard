"""Main entry point for the research platform."""

import asyncio
import logging
import sys

from .config.settings import Settings
from .core.orchestrator import PipelineOrchestrator


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger("research_platform")


async def main_async():
    """Async main function."""
    # Load settings
    settings = Settings.from_yaml("configs/production.yaml")

    # Setup logging
    logger = setup_logging(settings.log_level)

    logger.info("=" * 70)
    logger.info("Research Platform - Production Build")
    logger.info("=" * 70)
    logger.info(f"Organization: {settings.github_org}")
    logger.info(f"Python: {sys.version.split()[0]}")
    logger.info("")

    # Create orchestrator
    orchestrator = PipelineOrchestrator(settings, logger)

    try:
        # Run pipeline
        results = await orchestrator.run()

        # Print summary
        logger.info("=" * 70)
        logger.info("BUILD SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Phases completed: {results['completed_phases']}")
        logger.info(f"Total time: {results['total_time']:.2f}s")
        logger.info(f"Errors: {len(results['errors'])}")

        if results["errors"]:
            logger.error("Errors encountered:")
            for phase, error in results["errors"].items():
                logger.error(f"  {phase}: {error}")

        logger.info("=" * 70)

        # Exit with error code if there were failures
        return 1 if results["errors"] else 0

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return 1


def main():
    """Synchronous entry point."""
    exit_code = asyncio.run(main_async())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
