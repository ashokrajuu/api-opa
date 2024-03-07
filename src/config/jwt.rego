package jwt

import rego.v1

default allow := false

allow if {
	claims.role == "admin"
	input.method == "POST"
}


allow if {
	input.method == "GET"
	input.path == "/view"
	input.authenticated
}

claims := payload if {
	io.jwt.verify_hs256(bearer_token, input.secret_jwt)

	[_, payload, _] := io.jwt.decode(bearer_token)
}

bearer_token := t if {
	v := input.jwt_token
	startswith(v, "Bearer ")
	t := substring(v, count("Bearer "), -1)
}
