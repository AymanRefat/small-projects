from utils.option import Option
from utils.signal import Signal, Succeeded, Failed


def test_get_data_withnoinputs(opt_excute: Option):
    opt_excute.get_data()

    assert opt_excute.data_dict == {}


def test_start_success(opt_excute: Option):
    opt_excute.start()

    assert opt_excute.signal.__class__ == Succeeded


def test_start_failed(opt_raise_err: Option):
    opt_raise_err.start()

    assert opt_raise_err.signal.__class__ == Failed
