import discretisedfield as df
import micromagneticmodel as mm
import numpy as np


def test_simple_hysteresis_loop(calculator):
    """Simple hysteresis loop between Hmin and Hmax with symmetric number of steps."""
    system = mm.System(name="hysteresisdriver_noevolver_nodriver")

    A = 1e-12
    H = (0, 0, 1e6)
    system.energy = mm.Exchange(A=A) + mm.Zeeman(H=H)

    p1 = (0, 0, 0)
    p2 = (5e-9, 5e-9, 5e-9)
    n = (5, 5, 5)
    Ms = 1e6
    region = df.Region(p1=p1, p2=p2)
    mesh = df.Mesh(region=region, n=n)
    system.m = df.Field(mesh, nvdim=3, value=(0, 1, 0), norm=Ms)

    hd = calculator.HysteresisDriver()
    hd.drive(system, Hmin=(0, 0, -1e6), Hmax=(0, 0, 1e6), n=3)

    value = system.m(mesh.region.random_point())
    assert np.linalg.norm(np.subtract(value, (0, 0, Ms))) < 1e-3

    assert len(system.table.data.index) == 5

    assert system.table.x == "B_hysteresis"

    calculator.delete(system)
