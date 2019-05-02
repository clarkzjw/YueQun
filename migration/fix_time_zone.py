import pickle

from pony.orm import commit

from db.model import db_session, select, Message, db


def fix_time_zone():
    from datetime import datetime
    from pytz import timezone
    with db_session:
        all_messages = list(select(m for m in Message if 110099 < m.id <= 202868))
        print(len(all_messages))
        count = 1
        for m in all_messages:
            count += 1
            print(count)
            full_update = pickle.loads(m.tg_update_full)
            # timestamp = datetime.timestamp(full_update.message.date)
            timestamp = datetime.timestamp(full_update.message.date.replace(tzinfo=timezone("Asia/Shanghai")))
            m.set(tg_msg_timestamp=datetime.fromtimestamp(timestamp))
            commit()


if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    fix_time_zone()
