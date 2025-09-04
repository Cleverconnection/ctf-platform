package main

import (
	"encoding/json"
	"os"
	"strings"

	"github.com/ctfer-io/chall-manager/sdk"
	local "github.com/pulumi/pulumi-command/sdk/go/command/local"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
	sdk.Run(func(req *sdk.Request, resp *sdk.Response, opts ...pulumi.ResourceOption) error {
		env := pulumi.StringMap{}

		// Passa credenciais sempre que existirem
		pass := func(k string) {
			if v, ok := os.LookupEnv(k); ok && v != "" {
				env[k] = pulumi.String(v)
			}
		}
		for _, k := range []string{
			"PROXMOX_API_URL", "PROXMOX_USER", "PROXMOX_PASSWORD",
			"PROXMOX_TOKEN_ID", "PROXMOX_TOKEN_SECRET",
			"PROXMOX_VERIFY_SSL",
		} {
			pass(k)
		}

		// Set default se não vier do ambiente
		setOrDefault := func(k, def string) {
			if v := os.Getenv(k); v != "" {
				env[k] = pulumi.String(v)
			} else {
				env[k] = pulumi.String(def)
			}
		}

		// Defaults do seu ambiente/evento
		setOrDefault("PROXMOX_NODE", "cecpa")
		setOrDefault("PROXMOX_DATASTORE", "local-lvm")
		setOrDefault("TEMPLATE_VMID", "2210")
		setOrDefault("CLONE_MODE", "linked")
		setOrDefault("VM_CORES", "2")
		setOrDefault("VM_MEMORY_MB", "2048")
		setOrDefault("NET_BRIDGE", "vmbr0")
		setOrDefault("VMID_RANGE_START", "2200")
		setOrDefault("VMID_RANGE_END", "2300")
		// opcionais
		pass("NET_VLAN_TAG")
		pass("NIC_MODEL")
		pass("TTL_MINUTES")

		// Identidade do jogador/time (útil para logs)
		env["IDENTITY"] = pulumi.String(req.Config.Identity)

		// Executa seus scripts Python (create/destroy)
		cmd, err := local.NewCommand(req.Ctx, "proxmox-vm", &local.CommandArgs{
			Dir:         pulumi.String("."),
			Create:      pulumi.String("python3 create.py"),
			Delete:      pulumi.String("python3 destroy.py"),
			Environment: env,
		}, opts...)
		if err != nil {
			return err
		}

		// O que o create.py imprimir em stdout vira o connection_info (só o IP)
		out := cmd.Stdout.ApplyT(func(s string) string {
			s = strings.TrimSpace(s)
			var m map[string]any
			if json.Unmarshal([]byte(s), &m) == nil {
				// tenta extrair do JSON
				if v, ok := m["ip"]; ok {
					if str, ok := v.(string); ok && str != "" {
						return str
					}
				}
				if v, ok := m["connection_info"]; ok {
					if str, ok := v.(string); ok && str != "" {
						return str
					}
				}
				if v, ok := m["connectionInfo"]; ok {
					if str, ok := v.(string); ok && str != "" {
						return str
					}
				}
				if v, ok := m["address"]; ok {
					if str, ok := v.(string); ok && str != "" {
						return str
					}
				}
			}
			// fallback: devolve string crua
			return s
		}).(pulumi.StringOutput)

		resp.ConnectionInfo = out
		return nil
	})
}
