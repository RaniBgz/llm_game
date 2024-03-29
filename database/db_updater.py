from sqlalchemy import update
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from database.db_builder import NPC, Item

engine = create_engine('postgresql+psycopg2://rani:ranidb@localhost/llmgame')
Session = sessionmaker(bind=engine)
session = Session()

def get_npc_by_name(session, name):
    """
    Retrieves an NPC instance from the database by its name.

    Args:
        session (sqlalchemy.orm.session.Session): The SQLAlchemy session.
        name (str): The name of the NPC to retrieve.

    Returns:
        NPC: The NPC instance, or None if not found.
    """
    return session.query(NPC).filter_by(name=name).first()

def get_item_by_name(session, name):
    """
    Retrieves an Item instance from the database by its name.

    Args:
        session (sqlalchemy.orm.session.Session): The SQLAlchemy session.
        name (str): The name of the Item to retrieve.

    Returns:
        Item: The Item instance, or None if not found.
    """
    return session.query(Item).filter_by(name=name).first()

def update_npc_position(session, npc, global_position, local_position):
    """
    Updates the global and local position of an NPC instance in the database.

    Args:
        session (sqlalchemy.orm.session.Session): The SQLAlchemy session.
        npc (NPC): The NPC instance to update.
        global_position (str): The new global position in the format "x,y".
        local_position (str): The new local position in the format "x,y".
    """
    stmt = update(NPC).where(NPC.id == npc.id).values(
        global_position=global_position, local_position=local_position
    )
    session.execute(stmt)
    session.commit()

def update_item_description(session, item, new_description):
    """
    Updates the description of an Item instance in the database.

    Args:
        session (sqlalchemy.orm.session.Session): The SQLAlchemy session.
        item (Item): The Item instance to update.
        new_description (str): The new description for the Item.
    """
    stmt = update(Item).where(Item.id == item.id).values(description=new_description)
    session.execute(stmt)
    session.commit()

if __name__=="__main__":
    # Get an NPC by name
    npc = get_npc_by_name(session, "Elder")
    if npc:
        print(f"Found NPC: {npc.name}")
        # Update the NPC's position
        update_npc_position(session, npc, "2,3", "5,5")
    else:
        print("NPC not found")

    # Get an Item by name
    item = get_item_by_name(session, "Dagger")
    if item:
        print(f"Found Item: {item.name}")
        # Update the Item's description
        update_item_description(session, item, "A sharp iron dagger")
    else:
        print("Item not found")

    # Close the session
    session.close()