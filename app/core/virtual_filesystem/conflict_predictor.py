def detect_virtual_conflicts(vfs):

    conflicts = []

    seen = set()

    for file in vfs.all_files():

        simulated = file.simulated_name

        if simulated in seen:

            conflicts.append(simulated)

        seen.add(simulated)

    return conflicts