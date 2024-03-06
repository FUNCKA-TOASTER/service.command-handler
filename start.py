"""Service "toaster.comman-handling-service".
About:
    ...
    
Author:
    Oidaho (Ruslan Bashinskii)
    oidahomain@gmail.com
"""
import asyncio
from consumer import consumer
from handler import command_handler


async def main():
    """Entry point.
    """
    for data in consumer.listen_queue("commands"):
        command_handler(data)



if __name__ == "__main__":
    asyncio.run(main())
