import datetime
import motor.motor_asyncio
from config import Config
from helper.utils import send_log
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def admin_user(self, id):
        return dict(
            id=int(id),
            join_date=datetime.date.today().isoformat(),
            welc_file=None,
            leav_file=None,
            welcome=None,
            leave=None,
            bool_auto_accept=True,
            bool_welc=None,
            bool_leav=None,
            channel=[],
            admin_channels={},
        )

    def new_user(self, id):
        return dict(
            id=int(id),
            join_date=datetime.datetime.today().isoformat()
        )

    def approved_user(self, id):
        return dict(
            id=int(id)
        )

    async def set_welcome(self, user_id, welcome):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'welcome': welcome}})

    async def get_welcome(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('welcome', None)

    async def set_welc_file(self, user_id, welc_file):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'welc_file': welc_file}})

    async def get_welc_file(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('welc_file', None)

    async def set_leav_file(self, user_id, leav_file):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'leav_file': leav_file}})

    async def get_leav_file(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('leav_file', None)

    async def set_leave(self, user_id, leave):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'leave': leave}})

    async def get_leave(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('leave', None)

    async def set_bool_auto_accept(self, user_id, bool_auto_accept):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'bool_auto_accept': bool_auto_accept}})

    async def get_bool_auto_accept(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('bool_auto_accept', None)

    async def set_bool_welc(self, user_id, bool_welc):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'bool_welc': bool_welc}})

    async def get_bool_welc(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('bool_welc', None)

    async def set_bool_leav(self, user_id, bool_leav):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'bool_leav': bool_leav}})

    async def get_bool_leav(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('bool_leav', None)

    async def set_admin_channel(self, channel_id, condition):
        try:
            user = await self.col.find_one({'id': int(Config.ADMIN)})
            if user:
                channels = user.get('admin_channels', {})
                if channel_id not in channels:
                    channels.update({f'{channel_id}': condition})
                    await self.col.update_one({'id': int(Config.ADMIN)}, {'$set': {'admin_channels': channels}})
        except Exception as e:
            logger.error(f"Error in set_admin_channel: {e}")

    async def update_admin_channel(self, id, condition):
        try:
            user = await self.col.find_one({'id': int(Config.ADMIN)})
            if user:
                channels = user.get('admin_channels', {})
                if id in channels:
                    channels.update({f'{id}': condition})
                    await self.col.update_one({'id': int(Config.ADMIN)}, {'$set': {'admin_channels': channels}})
        except Exception as e:
            logger.error(f"Error in update_admin_channel: {e}")

    async def get_admin_channels(self):
        try:
            user = await self.col.find_one({'id': int(Config.ADMIN)})
            return user.get('admin_channels', {})
        except Exception as e:
            logger.error(f"Error in get_admin_channels: {e}")
            return {}

    async def remove_admin_channel(self, channel_id):
        try:
            user = await self.col.find_one({'id': int(Config.ADMIN)})
            if user:
                channels = user.get('admin_channels', {})
                if channel_id in channels:
                    channels.pop(channel_id)
                    await self.col.update_one({'id': int(Config.ADMIN)}, {'$set': {'admin_channels': channels}})
        except Exception as e:
            logger.error(f"Error in remove_admin_channel: {e}")

    async def set_channel(self, user_id, channel_id):
        try:
            user = await self.col.find_one({'id': int(user_id)})
            if user:
                channels = user.get('channel', [])
                if channel_id not in channels:
                    channels.append(channel_id)
                    await self.col.update_one({'id': int(user_id)}, {'$set': {'channel': channels}})
        except Exception as e:
            logger.error(f"Error in set_channel: {e}")

    async def get_channel(self, id):
        try:
            user = await self.col.find_one({'id': int(id)})
            return user.get('channel', [])
        except Exception as e:
            logger.error(f"Error in get_channel: {e}")
            return []

    async def remove_channel(self, user_id, channel_id):
        try:
            user = await self.col.find_one({'id': int(user_id)})
            if user:
                channels = user.get('channel', [])
                if channel_id in channels:
                    channels.remove(channel_id)
                    await self.col.update_one({'id': int(user_id)}, {'$set': {'channel': channels}})
        except Exception as e:
            logger.error(f"Error in remove_channel: {e}")

    async def add_user(self, b, m):
        try:
            u = m.from_user
            if not await self.is_user_exist(u.id):
                if u.id == Config.ADMIN:
                    user = self.admin_user(u.id)
                else:
                    user = self.new_user(u.id)
                await self.col.insert_one(user)
                await send_log(b, u)
        except Exception as e:
            logger.error(f"Error in add_user: {e}")

    async def add_appro_user(self, b, m):
        try:
            u = m.from_user
            if not await self.is_user_exist(u.id):
                user = self.approved_user(u.id)
                await self.col.insert_one(user)
                await send_log(b, u)
        except Exception as e:
            logger.error(f"Error in add_appro_user: {e}")

    async def is_user_exist(self, id):
        try:
            user = await self.col.find_one({'id': int(id)})
            return bool(user)
        except Exception as e:
            logger.error(f"Error in is_user_exist: {e}")
            return False

    async def total_users_count(self):
        try:
            count = await self.col.count_documents({})
            return count
        except Exception as e:
            logger.error(f"Error in total_users_count: {e}")
            return 0

    async def get_all_users(self):
        try:
            all_users = self.col.find({})
            return all_users
        except Exception as e:
            logger.error(f"Error in get_all_users: {e}")
            return []

    async def delete_user(self, user_id):
        try:
            await self.col.delete_many({'id': int(user_id)})
        except Exception as e:
            logger.error(f"Error in delete_user: {e}")


db = Database(Config.DB_URL, Config.DB_NAME)
