# DNS (Domain Name System)

## What is DNS?

DNS translates human-readable domain names to IP addresses.

```
www.google.com  →  DNS  →  142.250.185.36
(Domain Name)              (IP Address)
```

## DNS Resolution Flow

```
                              ┌──────────────┐
                              │  Root DNS    │
                              │  Server      │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │  TLD Server  │
                              │  (.com, .edu)│
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │ Authoritative│
                              │ Domain Server│
                              └──────────────┘
                                     ▲
                                     │
┌──────────┐      ┌──────────────┐   │
│   HOST   │ ←──→ │ DNS Resolver │───┘
│ (client) │      │              │
└──────────┘      └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    Cache     │
                  └──────────────┘
```

## Resolution Steps

1. **Host** sends query to **DNS Resolver** (usually your ISP or 8.8.8.8)
2. **Resolver** checks its **Cache** first
3. If not cached, queries the **Root DNS Server**
4. Root points to the **TLD Server** (.com, .edu, .org, etc.)
5. TLD points to the **Authoritative Domain Server**
6. Authoritative server returns the actual IP address
7. Resolver **caches** the result and returns it to the host

## DNS Hierarchy

```
         Root (.)
        /    \
     .com    .edu
      |        |
   google    mit
      |        |
   www      www
```

## Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | google.com → 142.250.185.36 |
| AAAA | IPv6 address | google.com → 2607:f8b0:... |
| CNAME | Alias | www.google.com → google.com |
| MX | Mail server | google.com → smtp.google.com |
| NS | Nameserver | google.com → ns1.google.com |
| TXT | Text data | SPF, DKIM, verification |

## Connections

- DNS names map to IPs in [IPv4 Subnetting](ipv4-subnetting.md) ranges
- VLANs ([VLAN Configuration](vlan-configuration.md)) can affect DNS resolution paths
- DNS is part of the networking layer that [BlackRoad's routing](../ai-architecture/agentic-patterns.md) builds upon
