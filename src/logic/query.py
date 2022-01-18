def query(circuit, c, q, num_array=[0, 1, 2, 3], num_state_array=2):
    i = 0
    ind = 0

    for x in num_array:
        if num_state_array == 3:
            if x < 4:
                circuit.cx(c[ind], q[i])
            i += 1
        if x < 2:
            circuit.cx(c[ind], q[i])
        i += 1
        if x % 2 == 0:
            circuit.cx(c[ind], q[i])
        i += 1
        ind += 1

    return circuit
