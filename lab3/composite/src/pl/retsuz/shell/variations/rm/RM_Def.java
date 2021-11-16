package pl.retsuz.shell.variations.rm;

import pl.retsuz.filesystem.Composite;
import pl.retsuz.filesystem.IComposite;
import pl.retsuz.shell.gen.ICommand;
import pl.retsuz.shell.variations.gen.CommandVariation;
import pl.retsuz.shell.variations.gen.ICommandVariation;

public class RM_Def extends CommandVariation {
    public RM_Def(ICommandVariation next, ICommand parent) {
        super(next, parent, "");
    }

    @Override
    public void make(String params) {
        Composite c = (Composite) (this.getParent().getContext().getCurrent());

        try {
            IComposite elem = c.findElementByPath(params);
            c.removeElement(elem);
            System.out.println("Usunięto");
        } catch (Exception e) {
            System.out.println("Docelowy element nie jest plikiem lub nie istnieje.");
        }
    }
}