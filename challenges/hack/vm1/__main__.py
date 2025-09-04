import pulumi
import pulumi_proxmoxve as proxmoxve

provider = proxmoxve.Provider("proxmox",
    endpoint="https://192.168.20.5:8006/",
    insecure=True,
    username="danilo@pve",
    password="Y@ra*2025"
)

vm = proxmoxve.vm.VirtualMachine("vm-ctf-teste",
    node_name="cecpa",
    vm_id=222,
    clone=proxmoxve.vm.VirtualMachineCloneArgs(
        vm_id=2200,
        full=True   # garante clone completo, independente do template
    ),
    cpu=proxmoxve.vm.VirtualMachineCpuArgs(
        cores=2
    ),
    memory=proxmoxve.vm.VirtualMachineMemoryArgs(
        dedicated=2048
    ),
    network_devices=[proxmoxve.vm.VirtualMachineNetworkDeviceArgs(
        bridge="vmbr0",
        model="e1000"
    )],
    opts=pulumi.ResourceOptions(provider=provider)
)

pulumi.export("ip_address", vm.ipv4_addresses)
