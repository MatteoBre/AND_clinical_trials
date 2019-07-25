import java.util.List;
import java.util.ArrayList;
import java.util.Vector;

import gov.nih.nlm.nls.tc.FilterApi.InputFilterOption;
import gov.nih.nlm.nls.tc.FilterApi.LegalWordsOption;
import gov.nih.nlm.nls.tc.FilterApi.OutputFilter;
import gov.nih.nlm.nls.tc.FilterApi.OutputFilterOption;

import gov.nih.nlm.nls.tc.Lib.Configuration;
import gov.nih.nlm.nls.tc.Lib.Count2f;

import gov.nih.nlm.nls.tc.Api.JdiApi;
import gov.nih.nlm.nls.tc.Api.StiApi;


public class APIWrapper {

    private JdiApi jdi;
    private StiApi sti;

    public APIWrapper(){
        this.jdi = new JdiApi("./Config/tc.properties");
        this.sti = new StiApi(new Configuration("./Config/tc.properties", false));
    }


    public List<String> getJDs(String text){
        Vector<Count2f> scores = jdi.GetJdiScoresByTextMesh(text, new InputFilterOption(LegalWordsOption.DEFAULT_JDI));

        OutputFilterOption outputFilterOption = new OutputFilterOption();
        outputFilterOption.SetOutputNum(100);

        String[] result = OutputFilter.ProcessText(scores, jdi.GetJournalDescriptors(), outputFilterOption).split("\n");

        List<String> journalDescriptors = new ArrayList<String>();

        for(String line : result){
            journalDescriptors.add(line);
        }
        return journalDescriptors;
    }


    public List<String> getSTs(String text){
        Vector<Count2f> scores = sti.GetStiScoresByText(text, new InputFilterOption(LegalWordsOption.DEFAULT_JDI));

        OutputFilterOption outputFilterOption = new OutputFilterOption();
        outputFilterOption.SetOutputNum(100);

        String[] result = OutputFilter.ProcessText(scores, sti.GetSemanticTypes(), outputFilterOption).split("\n");

        List<String> semanticTypes = new ArrayList<String>();

        for(String line : result){
            semanticTypes.add(line);
        }
        return semanticTypes;
    }

    public void close(){
        this.sti.Close();
        this.jdi.Close();
    }
}
