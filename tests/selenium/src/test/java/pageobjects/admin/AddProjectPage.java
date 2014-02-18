package pageobjects.admin;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;
import static org.junit.Assert.*;

/**
 * Author: Ruarcc McAloon
 * Date: 13/02/14
 * Time: 08:55
 */
public class AddProjectPage extends LoadableComponent<AllProjectsPage> {

    private WebElement title;
    private WebElement subtitle;
    private WebElement project_plan_summary;
    private WebElement background;
    private WebElement current_status;
    private WebElement project_plan;
    private WebElement sustainability;
    private WebElement target_group;
    private WebElement goals_overview;
    private WebElement _save;

    private WebDriver driver;
    private String url = "http://rsr.uat.akvo.org/admin/rsr/project/add/";
    private String pagetitle = "Add project | Akvo RSR site admin";

    public AddProjectPage(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    @Override
    protected void load() {
        this.driver.get(url);
    }

    @Override
    protected void isLoaded()  {
        assertTrue(driver.getTitle().equals(pagetitle));
    }

    /*
     * Expects an array of size 9 with following order:
     * [0] title
     * [1] subtitle
     * [2] project plan summary
     * [3] background
     * [4] current status
     * [5] project plan
     * [6] sustainability
     * [7] target group
     * [8] goals overview
     */
    public void fillInProjectDetails(String[] details){
        if(details.length != 9) {
            fail("Incorrect test data supplied, project details should be contained in array of size 9 - instead of: "+details.length);
        }

        title.sendKeys(details[0]);
        subtitle.sendKeys(details[1]);
        project_plan_summary.sendKeys(details[2]);
        background.sendKeys(details[3]);
        current_status.sendKeys(details[4]);
        project_plan.sendKeys(details[5]);
        sustainability.sendKeys(details[6]);
        target_group.sendKeys(details[7]);
        goals_overview.sendKeys(details[8]);
    }

    public void enterTitle(String value){
        title.sendKeys(value);
    }

    public void enterSubtitle(String value){
        subtitle.sendKeys(value);
    }

    public void enterProjectPlanSummary(String value){
        project_plan_summary.sendKeys(value);
    }

    public void enterBackground(String value){
        background.sendKeys(value);
    }

    public void enterCurrentStatus(String value){
        current_status.sendKeys(value);
    }

    public void enterProjectPlan(String value){
        project_plan.sendKeys(value);
    }

    public void enterSustainability(String value){
       sustainability.sendKeys(value);
    }

    public void enterTargetGroup(String value){
        target_group.sendKeys(value);
    }

    public void enterGoalsOverview(String value){
        goals_overview.sendKeys(value);
    }
}
