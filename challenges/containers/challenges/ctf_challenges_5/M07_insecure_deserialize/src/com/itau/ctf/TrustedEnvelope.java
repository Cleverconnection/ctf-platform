package com.itau.ctf;

import java.io.Serializable;

public class TrustedEnvelope implements Serializable {
    private static final long serialVersionUID = 20250125L;
    private String action;
    private String payload;

    public TrustedEnvelope() {
    }

    public TrustedEnvelope(String action, String payload) {
        this.action = action;
        this.payload = payload;
    }

    public String getAction() {
        return action;
    }

    public String getPayload() {
        return payload;
    }
}
