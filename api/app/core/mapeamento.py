from app.modelos.comando import CommandMapping


def build_command_mappings(topic_prefix: str) -> dict[str, CommandMapping]:
    """
    Cria o mapeamento dos 16 comandos MQTT para coils Modbus.

    Mapeamento adotado:

    Kit 1:
    - Pushbuttons 1 a 4 -> coils 0 a 3
    - Switches 1 a 4    -> coils 4 a 7

    Kit 2:
    - Pushbuttons 1 a 4 -> coils 8 a 11
    - Switches 1 a 4    -> coils 12 a 15

    A API sempre escreve no Kit 1.
    Os comandos do Kit 2 são enviados ao Kit 1, que deve repassar ao Kit 2.
    """

    mappings: dict[str, CommandMapping] = {}

    base_addresses = {
        ("kit1", "pushbutton"): 0,
        ("kit1", "switch"): 4,
        ("kit2", "pushbutton"): 8,
        ("kit2", "switch"): 12,
    }

    for kit in ["kit1", "kit2"]:
        for device_type in ["pushbutton", "switch"]:
            base_address = base_addresses[(kit, device_type)]

            for number in range(1, 5):
                key = f"{kit}.{device_type}.{number}"
                topic = f"{topic_prefix}/{kit}/{device_type}/{number}"
                coil_address = base_address + (number - 1)

                mappings[key] = CommandMapping(
                    key=key,
                    kit=kit,
                    device_type=device_type,
                    number=number,
                    topic=topic,
                    coil_address=coil_address,
                    description=f"{device_type} {number} do {kit}",
                )

    return mappings
