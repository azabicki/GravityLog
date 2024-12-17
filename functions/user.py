import os
from datetime import datetime
import streamlit as st
import pandas as pd
import functions.data as data
import functions.utils as utils


def select_user(src: str, del_idx: int) -> None:
    """
    Updates the active user according to source:

    "sidebar":
        Selectbox in the sidebar changed: new user selected, change session state user

    "deletion":
        Delete button was used: deleted user was active, new user to be selected

    When user changes:
        - update session state user index/name/height/target/trend-data
        - load db for selected user

    Args:
        src (str): Source of the call "sidebar" | "deletion"
        del_idx (int): Index of the user deleted, determines new user selection

    Returns:
        None
    """

    match src:
        # from sidebar
        case "sidebar":
            idx = st.session_state["sb_user"]

        # from sidebar
        case "deletion":

            # last user deleted
            if len(st.session_state.user_db) == 0:
                idx = None

            # deleted used was ABOVE active
            elif del_idx <  st.session_state.user_idx:
                idx = st.session_state.user_idx-1

            # deleted used was UNDER active
            elif del_idx > st.session_state.user_idx:
                idx = st.session_state.user_idx

            # deleted user was EQUAL active
            else:
                nUser = len(st.session_state.user_db)-1
                idx = del_idx if del_idx < nUser else nUser

        case _:
            idx = None

    # update user
    st.session_state.user_idx = idx

    # update user settings
    utils.set_user_sessionstate()

    # load user db
    if st.session_state.user_idx is not None:
        st.session_state.db = data.load()
    else:
        st.session_state.db = data.create_df()


def load_db() -> pd.DataFrame:
    """
    Load the user database from CSV file.

    Reads and returns the users.csv file which contains user profiles and settings.

    Returns:
        pd.DataFrame: DataFrame containing user data from users.csv
    """

    # return pd.read_csv(os.path.join("data", "usersBSK.csv"))
    return pd.read_csv(os.path.join("data", "users.csv"))


def add(name:str, height:int, target:int) -> None:
    """
    Add a new user to the database and create a new CSV file for user measurements.

    Takes the user's name, height, and target weight, creates a new entry in the user database with default trend settings, and generates a blank measurement CSV file for the new user.

    If the user name already exists, sets a flag and returns without making changes.

    Args:
        name (str): Name of the user to add
        height (int): Height of the user in centimeters
        target (int): Target weight of the user in kilograms

    Returns:
        None

    Side Effects:
        - Creates new user entry in users.csv
        - Creates new blank CSV file for user measurements
        - Updates session state user database
        - Sets success/error flags in session state
    """

    # return if user already exists
    if name in st.session_state.user_db["name"].values:
        st.session_state.flags["usr_add_exists"] = True
        return

    # set flag
    st.session_state.flags["usr_add_ok"] = True

    # reset session state variables
    st.session_state["new_usr_name"] = ""
    st.session_state["new_usr_height"] = 180
    st.session_state["new_usr_target"] = 80

    # new row for user
    new_user = pd.DataFrame.from_records({
        "name": name,
        "height": height,
        "target": target,
        "trend_how": "date_range",
        "trend_start": datetime.now().date(),
        "trend_range": 4
    },index=[0])

    # add row to users_db
    st.session_state.user_db = pd.concat([st.session_state.user_db, new_user], ignore_index=True)

    # save users.csv
    st.session_state.user_db.to_csv(os.path.join("data", "users.csv"), index=False)

    # create new csv for new user
    new_db = data.create_df()
    new_db.to_csv(os.path.join("data", name + ".csv"), index=False)


def update_user() -> None:
    """
    Updates the data of a user in the user database.

    Takes edited rows from the session state's user_edited dictionary,
    applies them to the user database, and saves the updated data to the users.csv file.
    Also updates the active user's height and target weight in session state if they were modified.

    Returns:
        None
    """

    # first, process edited cells and create temporary df
    st.session_state.user_db = st.session_state.user_db.copy()
    edt = st.session_state.user_edited["edited_rows"]
    for idx, dct in edt.items():
        for col, val in dct.items():
            st.session_state.user_db.loc[idx, col] = val

    # set flag
    st.session_state.flags["usr_update_ok"] = True

    # update user_db and user_data in session_state
    st.session_state.user_cm = st.session_state.user_db.loc[st.session_state.user_idx, "height"]
    st.session_state.user_kg = st.session_state.user_db.loc[st.session_state.user_idx, "target"]

    # save users.csv
    st.session_state.user_db.to_csv(os.path.join("data", "users.csv"), index=False)



def delete(idx: int|None) -> None:
    """
    Deletes a user from the user database and removes their csv file.

    Args:
        idx (int|None): Index of user to delete in the user database dataframe.
            If None, resets session state variables and returns.

    Returns:
        None
    """

    # if idx is None, reset session state variables and return
    if idx is None:
        st.session_state.sb_user_delete = None
        return

    # remove user's data csv file
    os.remove(os.path.join("data", st.session_state.user_db.loc[idx, "name"] + ".csv"))

    # delete user from user_db
    print(st.session_state.user_db)
    st.session_state.user_db = st.session_state.user_db.drop(idx).reset_index(drop=True)
    print(st.session_state.user_db)

    # save users.csv
    st.session_state.user_db.to_csv(os.path.join("data", "users.csv"), index=False)

    # handle 'active user' when deleted user was active user
    print("___handle active user, deleted: ", idx)
    select_user(src="deletion", del_idx=idx)

    # set flag
    st.session_state.flags["usr_del_ok"] = True
