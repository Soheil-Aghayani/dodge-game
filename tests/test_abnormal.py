import pytest
from module.abnormal import AbnormalManager

def test_activate_manual_valid_type():
    manager = AbnormalManager()
    for abnormal_type in manager.ABNORMAL_TYPES:
        manager.activate_manual(abnormal_type)
        assert manager.abnormal_type == abnormal_type
        assert manager.active is True
        assert manager.manual_mode is True
        assert manager.last_abnormal_type == abnormal_type

def test_activate_manual_invalid_type():
    manager = AbnormalManager()
    manager.activate_manual('invalid_type')
    assert manager.abnormal_type is None
    assert manager.active is False
    assert manager.manual_mode is False
    assert manager.last_abnormal_type is None

def test_deactivate_manual():
    manager = AbnormalManager()
    manager.activate_manual('reverse_floor')
    manager.deactivate_manual()
    assert manager.active is False
    assert manager.manual_mode is False
    assert manager.abnormal_type is None

def test_update_manual_mode():
    manager = AbnormalManager()
    manager.activate_manual('reverse_floor')

    # Save state
    abnormal_type = manager.abnormal_type
    active = manager.active
    manual_mode = manager.manual_mode
    last_abnormal_type = manager.last_abnormal_type

    # Call update, it should return early
    manager.update(500)

    # Verify state didn't change
    assert manager.abnormal_type == abnormal_type
    assert manager.active == active
    assert manager.manual_mode == manual_mode
    assert manager.last_abnormal_type == last_abnormal_type
