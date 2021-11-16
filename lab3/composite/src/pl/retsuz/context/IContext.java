package pl.retsuz.context;

import pl.retsuz.filesystem.IComposite;

public interface IContext {
    public IComposite getCurrent();

    public void setCurrent(IComposite current);
}
