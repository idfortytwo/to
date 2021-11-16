package pl.retsuz.shell.variations.mv;

import pl.retsuz.filesystem.Composite;
import pl.retsuz.filesystem.IComposite;
import pl.retsuz.shell.gen.ICommand;
import pl.retsuz.shell.variations.gen.CommandVariation;
import pl.retsuz.shell.variations.gen.ICommandVariation;

public class MV_Path extends CommandVariation {
    public MV_Path(ICommandVariation next, ICommand parent) {
        super(next, parent, "[a-zA-Z0-9.l\\/_]* [a-zA-Z0-9.l\\/_]*");
    }

    @Override
    public void make(String params) {
        Composite c = (Composite) (this.getParent().getContext().getCurrent());
        String[] tab = params.split(" ");
        String sourcePath = tab[0], destinationPath = tab[1];

        IComposite source, destination;

        try {
            source = c.findElementByPath(sourcePath);
        } catch (Exception e) {
            System.out.println("Element źródłowy nie istnieje");
            return;
        }

        try {
            destination = c.findElementByPath(destinationPath);
        } catch (Exception e) {
            System.out.println("Ścieżka docelowa nie istnieje");
            return;
        }

        try {
            Composite.moveElement(source.getParent(), destination, source);
        } catch (Exception e) {
            System.out.println("mv nie powiodło się");
            e.printStackTrace();
        }

        System.out.println("Przeniesiono");
    }
}