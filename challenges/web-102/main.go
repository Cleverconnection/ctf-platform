package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/ctfer-io/chall-manager/sdk"
	local "github.com/pulumi/pulumi-command/sdk/go/command/local"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
	sdk.Run(func(req *sdk.Request, resp *sdk.Response, opts ...pulumi.ResourceOption) error {
		// ---------- Ambiente base passado aos scripts ----------
		env := pulumi.StringMap{}

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
		setOrDefault := func(k, def string) {
			if v := os.Getenv(k); v != "" {
				env[k] = pulumi.String(v)
			} else {
				env[k] = pulumi.String(def)
			}
		}
		setOrDefault("PROXMOX_NODE", "cecpa")
		setOrDefault("PROXMOX_DATASTORE", "local-lvm")
		setOrDefault("TEMPLATE_VMID", "2210")
		setOrDefault("CLONE_MODE", "linked")
		setOrDefault("VM_CORES", "2")
		setOrDefault("VM_MEMORY_MB", "2048")
		setOrDefault("NET_BRIDGE", "vmbr0")
		setOrDefault("VMID_RANGE_START", "2200")
		setOrDefault("VMID_RANGE_END", "2300")
		pass("NET_VLAN_TAG")
		pass("NIC_MODEL")
		pass("TTL_MINUTES")

		// Identidade (aparece nos logs do CM)
		env["IDENTITY"] = pulumi.String(req.Config.Identity)

		// ---------- RECURSO 1: CREATE ----------
		createCmd, err := local.NewCommand(req.Ctx, "proxmox-vm-create", &local.CommandArgs{
			Dir:         pulumi.String("."),
			Create:      pulumi.String("python3 create.py"),
			Environment: env,
		}, opts...)
		if err != nil {
			return err
		}

		// Parse do stdout do create.py
		type out struct {
			IP              string      `json:"ip"`
			VMID            interface{} `json:"vmid"`
			ConnectionInfo  string      `json:"connectionInfo"`
			ConnectionInfo2 string      `json:"connection_info"`
			Address         string      `json:"address"`
		}

		ipOut := createCmd.Stdout.ApplyT(func(s string) string {
			s = strings.TrimSpace(s)
			var o out
			if json.Unmarshal([]byte(s), &o) == nil {
				if o.IP != "" {
					return o.IP
				}
				if o.ConnectionInfo != "" {
					return o.ConnectionInfo
				}
				if o.ConnectionInfo2 != "" {
					return o.ConnectionInfo2
				}
				if o.Address != "" {
					return o.Address
				}
			}
			// fallback: string inteira (não recomendável, mas evita quebrar)
			return s
		}).(pulumi.StringOutput)

		vmidOut := createCmd.Stdout.ApplyT(func(s string) string {
			var o out
			if json.Unmarshal([]byte(s), &o) == nil {
				switch v := o.VMID.(type) {
				case float64:
					return fmt.Sprintf("%.0f", v)
				case string:
					return strings.TrimSpace(v)
				default:
					var m map[string]any
					if json.Unmarshal([]byte(s), &m) == nil {
						if vv, ok := m["vmid"]; ok {
							return fmt.Sprintf("%v", vv)
						}
					}
				}
			}
			return ""
		}).(pulumi.StringOutput)

		// Exporta para o stack (útil p/ observabilidade/jenitor)
		req.Ctx.Export("vmid", vmidOut)
		req.Ctx.Export("ip", ipOut)

		// O plugin do CTFd só lê connection_info/connectionInfo (string)
		resp.ConnectionInfo = ipOut

		// ---------- RECURSO 2: DELETE ----------
		// Passamos explicitamente OUTPUTS_JSON para o destroy.py com vmid/ip do create
		outputsJSON := pulumi.Sprintf(`{"vmid": %s, "ip": "%s"}`, vmidOut, ipOut)

		// Clona env e adiciona OUTPUTS_JSON
		envForDelete := pulumi.StringMap{}
		for k, v := range env {
			envForDelete[k] = v
		}
		envForDelete["OUTPUTS_JSON"] = outputsJSON

		_, err = local.NewCommand(req.Ctx, "proxmox-vm-destroy", &local.CommandArgs{
			Dir:         pulumi.String("."),
			Delete:      pulumi.String("python3 destroy.py"),
			Environment: envForDelete,
		}, append(opts, pulumi.DependsOn([]pulumi.Resource{createCmd}))...)
		if err != nil {
			return err
		}

		return nil
	})
}
