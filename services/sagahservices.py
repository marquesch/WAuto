def multiple_create_and_add_unities(sagah_unities_disc_list):
    from services.util import sagahutil
    created_disc_list = []
    sagahutil.login()
    for disc in sagah_unities_disc_list:
        unity_list = disc['disc_ua_list']
        disc_name = disc['disc_name']
        create_and_add_unities(disc_name, unity_list)
        created_disc_list.append(disc_name)
    sagahutil.driver_quit()
    return created_disc_list


def create_and_add_unities(disc_name, unities: list, login=False, quit=False):
    from services.util import sagahutil
    if login:
        sagahutil.login()
    sagahutil.create_disc(disc_name)
    disc_size = str(len(unities))
    sagahutil.edit_disc_size(disc_name, disc_size)
    for unity in unities:
        sagahutil.add_unity(disc_name, unity)
    sagahutil.approve_disc(disc_name)
    if quit:
        sagahutil.driver_quit()
