package pl.retsuz.shell.variations.mkdir;

import pl.retsuz.filesystem.Composite;
import pl.retsuz.filesystem.IComposite;
import pl.retsuz.shell.gen.ICommand;
import pl.retsuz.shell.variations.gen.CommandVariation;
import pl.retsuz.shell.variations.gen.ICommandVariation;

public class Mkdir_Path extends CommandVariation {
    public Mkdir_Path(ICommandVariation next, ICommand parent) {
        super(next, parent, "[a-zA-Z0-9.l\\/_]*");
    }

    @Override
    public void make(String params) {
        Composite c = (Composite) (this.getParent().getContext().getCurrent());
        String[] path = params.split("/");

        for (String path_node : path) {
            Composite node;
            try {
                node = (Composite) c.findElementByPath(path_node);
                c = (Composite) c.getElement(node);
            } catch (Exception e) {
                node = new Composite();
                node.setName(path_node);
                try {
                    c.addElement(node);
                    c = (Composite) c.getElement(node);
                } catch (Exception ex) {
                    System.out.println("mkdir nie powiodło się");
                    ex.printStackTrace();
                }
            }
        }

        System.out.println("Stworzono");
    }
}