# How I build (Mermaid version)

Native alternative to `architecture-dark.svg` / `architecture-light.svg`.
GitHub renders Mermaid natively and adapts it to the viewer's theme. To use it
on the profile, paste the block below into `README.md` in place of the
`<picture>` under **How I build**.

```mermaid
flowchart LR
    subgraph APPS_L["Side-by-side apps"]
        direction TB
        KT["<b>Kotlin · Android</b><br/>Warehouse apps on SAP EWM"]
        PY["<b>Python · Streamlit</b><br/>Finance & HR automation"]
        JV["<b>Java</b><br/>Backend services"]
    end

    subgraph INT["Integration layer"]
        direction TB
        OD["OData"]
        CA["Communication Arrangements"]
        BTP["SAP BTP"]
        IS["Integration Suite"]

        subgraph CORE["SAP S/4HANA Public Cloud Edition — Clean Core"]
            direction TB
            ABAP["ABAP Cloud"]
            RAP["RAP"]
            CDS["CDS Views"]
            DOM["EWM · MM"]
        end
    end

    subgraph APPS_R["Side-by-side apps"]
        direction TB
        FE["<b>Fiori Elements · Web</b><br/>Angular · React · TypeScript"]
        SF["<b>Salesforce</b><br/>CRM integration"]
        AI["<b>AI · MCP</b><br/>LLM agents"]
    end

    KT <--> OD
    PY <--> OD
    JV <--> CA
    OD <--> CORE
    CA <--> CORE
    BTP <--> CORE
    IS <--> CORE
    FE <--> OD
    SF <--> CA
    AI <--> BTP

    classDef core fill:#0070F2,stroke:#0070F2,color:#ffffff
    classDef int fill:#0E7490,stroke:#22D3EE,color:#ffffff
    classDef app fill:#0A1628,stroke:#2A5A8F,color:#E6EEF8
    class ABAP,RAP,CDS,DOM core
    class OD,CA,BTP,IS int
    class KT,PY,JV,FE,SF,AI app
```
