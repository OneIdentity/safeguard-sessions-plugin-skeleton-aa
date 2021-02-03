from ...plugin_bare import Plugin

def test_authenticate_accepts():
    config=''
    parameters=dict(
        cookie={},
        session_cookie={},
        gateway_user='somebody',
        key_value_pairs={'otp': ''},
    )

    result = Plugin(config).authenticate(**parameters)
    assert result['verdict'] == 'ACCEPT'
