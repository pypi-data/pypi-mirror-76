
class BaseAdmin{

    constructor(data){    
        this.cmsentry = data;
        this.cmsentry_id = data["id"];
          
    }
}


class Admin extends BaseAdmin{
    
    constructor(data){
        super(data);
    }

    //display the admin page
    show(){
        this.pre_show();
        document.getElementById("overlay").style.display = "block";
        this.post_show();
        this.register_click_handlers();
        
        
        log.debug("CMSEntry for page is: ", this.cmsentry);
        
    }

    hide(){
        document.getElementById("overlay").style.display = "none";
    }

    pre_show(){
    
    }
    
    post_show(){
        log.debug("Admin post show");
    }
}

/** 
An Admin class implements the whole admin interface view for each pagetype. 
The name matches the page for its purpose.
**/

class CategoryPageAdmin extends Admin{

    constructor(data){
        super(data);
        this.x = "An X";
    }
    
    post_show(){
        this.cmsEditorWidget = new CMSEditorWidget(this.cmsentry);
        this.cmsEditorWidget.updateContentEditor();
        
        this.cmsEntriesWidget = new CMSEntriesWidget(this.cmsentry);
        this.cmsEntriesWidget.update();
        
        this.cmsFileUploaderAdmin = new CMSFileUploaderAdmin(this.cmsentry);
    }
    
    register_click_handlers(){
        console.log("Registered handles");
        var cmsEditorWidget = this.cmsEditorWidget;
        var cmsEntriesWidget = this.cmsEntriesWidget;
        $("#editor-save-button").click((event) =>{cmsEditorWidget.save();})
        $("#published_checkbox").click((event) =>{cmsEditorWidget.toggle_published(); event.stopPropagation();})
        $("#frontpage_checkbox").click((event) =>{cmsEditorWidget.toggle_frontpage(); event.stopPropagation();})
        $("#create-cms-entry-button").click((event) => {cmsEntriesWidget.create_cms_entry(); })
        $("#createpage_title").focusout((event) => {cmsEntriesWidget.create_page_title_focus_out(); })
        $(".table_entry_published").click(function(){ cmsEntriesWidget.toggle_table_entry_published(); }); 
        $(".table_entry_frontpage").click(function(){ cmsEntriesWidget.toggle_table_entry_frontpage(); }); 
        $("#content-editor").keydown((event)=>{ cmsEditorWidget.handleKeyDownEvent(event); event.stopPropagation();});
        
          $(document).on('click','td',function() {
            log.debug('clicked', this.getAttribute("class"));
            
            if (this.getAttribute("class") == "table_entry_frontpage"){ 
                cmsEntriesWidget.toggle_table_entry_frontpage(this);
                }
            else{
            if (this.getAttribute("class") == "table_entry_published"){ 
                cmsEntriesWidget.toggle_table_entry_published(this);
                }           
            }
        });
    }
    
}

class SinglePageAdmin extends Admin{


}


/** A Base class for all Admin widget 
Common methods needed are refactored to here.
**/

class AdminWidget{


    /** Turns string into a slug **/
    string_to_slug (str) {
        str = str.replace(/^\s+|\s+$/g, ''); // trim
        str = str.toLowerCase();
    
        // remove accents, swap ñ for n, etc
        var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
        var to   = "aaaaeeeeiiiioooouuuunc------";
        for (var i=0, l=from.length ; i<l ; i++) {
            str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
        }
    
        str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
            .replace(/\s+/g, '-') // collapse whitespace and replace by -
            .replace(/-+/g, '-'); // collapse dashes
    
        return str;
    }

}


/** 
Implements the actions for a CMSEntryEditor widget.
The HTML assumes to have  the following elements.  
    #editor-save-button  - a button to save
    #published_checkbox - a checkbox to show published attribute
    #frontpage_checkbox - a checkbox to show frontpage attribute
    #content-editor  - a textarea for displaying the editable content.
**/





function set_admin_message_alert(message){

    log.debug("Setting admin message:", message);
    $("#admin-message-alert").text(message);
     $("#admin-message-alert").show();
   setTimeout(hide_admin_message_alert, 2000);
    
}       


function hide_admin_message_alert(){
    $("#admin-message-alert").hide(); 
}
    

class CMSEditorWidget extends AdminWidget{
    
    constructor(value){
        super(value);
        this.cmsentry = value;
        this.content_id = this.cmsentry["content"]["0"];    
    
        var published = this.cmsentry.published;
        var frontpage = this.cmsentry.frontpage;
        
        $("#published_checkbox").prop('checked', this.cmsentry.published);
        $("#frontpage_checkbox").prop('checked', this.cmsentry.frontpage);  
        
        
    }

    save(){
  
        log.debug("#editor-save-button pressed CMSEditorWidget->save() invoked")
        var content_txt = $("#content-editor").val();
        var start = Date.now();
        log.debug(content_txt);
        
        var data = { "content": content_txt,};
            url = "/cms/api/v2/cmscontents/" + this.content_id + "/";
             $.ajax({
            url: url,
            type: 'PUT',
            data: data,
    
            error: function(data){
                log.error("Ajax PUT failed:" + url , data);
                $("#editor_message_pane").html("Failed to save  content with error:." + data);
                log.debug("Failed to save  content with error:." + data);
                set_admin_message_alert("Error saving document.");
            },
            success: (data)=>{
                /**Update the editor for the newly created pages.**/
               log.debug("Ajax PUT success: " + url , data);;
               var completed = Date.now()
               var seconds = ( completed - start)/1000;
                log.debug("Content was successfully saved..(" + seconds  + "s) "+ completed.toLocaleString());
                
                set_admin_message_alert("Content saved..");
            }
        });
    }
    
    
     handleKeyDownEvent(event){
        /** 
        Handles keyboard events for the content-editor. 
        **/
       
        var tab_spaces = 4;  
        var editor  = $("#content-editor");
        
        if(event.keyCode === 9) { // tab was pressed
            /** 
            When tab is pressed, insert 4 spaces.
            **/
            var start = editor.prop("selectionStart");
            var end = editor.prop("selectionEnd");
            console.log("selectionStart: ", start);
            console.log("selectionEnd: ", end);
            // set textarea value to: text before caret + 4 spaces + text after caret
          
            var indented = "";
            var selection = editor.val().substring(start, end);
            
            if (start != end){
                console.log("start not end ==============================");
                var ks = selection.split(/\r?\n/);
            console.log(" line : ",ks);
                var num_lines = ks.length;
                for (var i=0; i < num_lines; i++){
                    indented = indented + "    " + ks[i] + "\r\n";
                }
            }else
            {
                indented = "    ";
            }
            
                
            console.log(selection);
                      editor.val(editor.val().substring(0, start)
                        + indented + selection 
                        + editor.val().substring(end));
            
            
        
        
        
            // put caret at right position again
            editor.prop("selectionStart",start + tab_spaces) ;
            editor.prop("selectionEnd", end + tab_spaces) ;
        
        
            // prevent the focus lose
            //editor.focus(); //This did not work to regain focus
            //return false;   //This did not work to regain focus
            //Found a solution and explanation here: https://stackoverflow.com/questions/8380759/why-isnt-this-textarea-focusing-with-focus
            event.preventDefault();
            
            
        }    
    }

    toggle_published(){
    
        url = "/cms/api/v2/cmsentries/" + this.cmsentry.id + "/";
        var published_status = $("#published_checkbox").is(':checked');
        
        log.debug("Setting published to:", published_status);
 
        $.ajax({
            url: url,
            type: 'PATCH',
            data: { published : published_status },
    
            error: function(data){ 
                log.debug("Publishe toggle failed.", data);
                 set_admin_message_alert("Failed to publish");
            },
            
            success: (data) => {
                log.debug("Set published to :" ,data);
                this.cmsentry.published = data["published"];
                
                if ( published_status == false){
                    set_admin_message_alert("Article unpublished");    
                }  else {
                    set_admin_message_alert("Article published");
                }
            }
        });
    
    }
    
    toggle_frontpage(){
    
        url = "/cms/api/v2/cmsentries/" + this.cmsentry.id + "/";
        var frontpage_status = $("#frontpage_checkbox").is(':checked');
        
        log.debug("Setting frontpage to:", frontpage_status)
 
        $.ajax({
            url: url,
            type: 'PATCH',
            data: { frontpage : frontpage_status },
    
            error: function(data){ 
                log.debug("Frontpage toggle failed.", data);
                 set_admin_message_alert("Could not set to frontpage");
                
                
            },
            
            success: (data) => {
                log.debug("Set frontpage to :" ,data);
                this.cmsentry.frontpage = data["frontpage"];
                if ( frontpage_status == false){
                    set_admin_message_alert("Article unpublished");    
                }  else {
                    set_admin_message_alert("Article published");
                }
            }
        });
    }
    
    updateContentEditor(id){
    
        log.debug("updateContentEditor: this = ", this);
        url = "/cms/api/v2/cmscontents/" + this.content_id + "/";
        log.debug("updateContentEditor fetching: ", url);
        $.ajax({
            url: url,
            type: 'GET',
            error: function(){
                log.debug("updateContentEditor: Failed to get cmscontent object from:", url);
            },
            success: function(data){
             log.debug("updateContentEditor success:", data);
                var content = data["content"];
                //log.debug(content);
                $("#content-editor").text(content);
                
            }
        });  
    }
    
   
}


/** Implements the actions for CMSEntries widget **/
class CMSEntriesWidget extends AdminWidget{

    constructor(cmsentry){
        super()
        this.cmsentry = cmsentry;
      
   
    }
    
    create_page_title_focus_out(){
    
        var title = $("#createpage_title").val();
        var slug = this.string_to_slug(title);
        $("#createpage_slug").val(slug);   
    }
    
    
    toggle_table_entry_published(element){
        
        var id = $(element).closest('tr').attr("id");
        var status_str = element.textContent;
        url = "/cms/api/v2/cmsentries/" + id + "/";
       
        var bool_status;
        //Use the status from the page?
        if (status_str == "true"){
            bool_status = false;
        }
        else{
            bool_status= true;
        }
        
        
        url = "/cms/api/v2/cmsentries/" + id + "/";
        
        $.ajax({
            url: url,
            type: 'PATCH',
            data: { published : bool_status },
    
            error: function(data){ 
                log.debug("CMSEntryWidget Publish toggle failed.", data);  
            },
            
            success: (data) => {
                log.debug("CMSEntry Set frontpage to :" ,data);
                element.textContent=data["published"] ;
            }
        });
        
    }
    
    toggle_table_entry_frontpage(element){
    
        var id = $(element).closest('tr').attr("id");
        var status_str = element.textContent;
        url = "/cms/api/v2/cmsentries/" + id + "/";
       
        var bool_status;
        //Use the status from the page?
        if (status_str == "true"){
            bool_status = false;
        }
        else{
            bool_status= true;
        }
        
        
        url = "/cms/api/v2/cmsentries/" + id + "/";
        
        $.ajax({
            url: url,
            type: 'PATCH',
            data: { frontpage : bool_status },
            error: function(data){ 
                log.debug("CMSEntryWidget frontpage toggle failed.", data);  
            },            
            success: (data) => {
                log.debug("CMSEntry Set frontpage to :" ,data);
                element.textContent=data["frontpage"] ;
            }
        });
    }
    
    
    
    /** 
        Gets the list of all CMSEntries that have the current CMSEntry as 
        parent
    **/
    update(){
            
        var path_id = view_json["path"];
        var url = "/cms/api/v2/cmsentries/?limit=100&parent_path_id="+path_id;
        console.log("GOING TO FETCH", url);
       
        console.log(this.cmsentry);
        $.ajax({
            url: url,
            type: 'GET',
            error: function(){
                log.debug("Failed to get CMSEntries");
            },
            success: function(cmsentries){
                log.debug("CMSEntries",cmsentries);
    
                var cmsentries_list = cmsentries["results"];
                /**We also want to get the CMSPageTypes to use in our display **/
                
                console.log("GOT RESILTS", cmsentries_list);
                $.ajax({
                    url: "/cms/api/v2/cmspagetypes/",
                    type: 'GET',
                    error: function(){
                        log.debug("Failed to load PageTypes");
                    },
                        
                    success: function(data){
                
                        log.debug("Got PageTypes: ", data);
            
                        var pagetypes = data["results"];
            
                        $('#CMSEntriesTable tbody').empty();
                    
                        /** create an index **/
                        
                        var pagetype_dict = {};
                        
                        for (var j=0; j < pagetypes.length; j++){
                                //log.debug(pagetypes[j]);
                                /**if (pagetypes[j]["id"] == pagetype_id){
                                    log.debug("PAGETYPE: ",pagetypes[j].page_type);
                                    var pagetype_text = pagetypes[j]["text"];
                                }**/
                                
                                pagetype_dict[pagetypes[j]["id"]] = pagetypes[j]["text"]; 
                                
                            }
            
                     
                        log.debug(pagetype_dict);
                        for (var i=0; i < cmsentries_list.length; i++){
                            var entry = cmsentries_list[i]; 
                            var pagetype_id = entry.page_type;
                            
                            var table_row = "<tr id=\"" + entry.id + "\"><td>" + entry.id + "</td>";
            
                            var title_link = "<a href=\"/cms"+ entry.path + "\">" + entry.title + "</a>"
                            table_row = table_row + "<td>" + title_link + "</td>";
                            table_row = table_row + "<td>" + pagetype_dict[entry.page_type] + "</td>";
                            table_row = table_row + "<td class=\"table_entry_published\">"+ entry.published +"</td>";
                            table_row = table_row + "<td class=\"table_entry_frontpage\">"+ entry.frontpage +"</td>";
                            table_row = table_row + "<td>"+ entry.date_created +"</td></tr>";            
                            //log.debug("Adding : " + table_row)
                            $('#CMSEntriesTable tbody:last-child').append(table_row);
                        }
                    }
                });
            }
        });
    }

    create_cms_entry(){
        var title = $("#createpage_title").val();
        var slug = $("#createpage_slug").val();
        var page_type = $('select[name=createpage_pagetype_select]').val();

        var fake=true
        var data = {
             title: title ,
             slug : slug,
             content: [ ],
             page_type: page_type,
            frontpage: false,
            published: false,
            page_number: 0,
            fake: true
            };
            
        var fake="?fake=true"

        var url = "/cms/api/v2/cmsentries/" + this.cmsentry.id + "/create_child/" + fake;
        
        console.log(url);
         $.ajax({
            url: url,
            type: 'POST',
            data: data,
    
            error: function(data){
                log.debug("Category Child Creation Failed with error", data);
            },
            success: (data) =>{
                
                this.update();
            
            }
        });

    }


}


class CMSFileUploaderAdmin{
    constructor(cmsentry){
        var self=this;
        self.cmsentry = cmsentry;
        
        self.url = "/cms"+ cmsentry.path + "/assets_manager/";
        $.ajax({
            url: self.url,
            type: 'GET',
            error: function(){
              console.log("Failed to get assets manager API endpoint", self.url);
            },
            success: function(data){
               
                var content = data["categories"];
                
                console.log("DATA ", data);
                
                self.initialPreviewConfigData = data["initialPreviewConfig"];
                self.initialPreviewData = data["initialPreview"];
                self.update();
            }
        });
    }

    update(){
    
    
        $("#kv-explorer").fileinput({
            'theme': 'explorer-fas',
            'uploadUrl': 'assets_manager/',
            overwriteInitial: false,
            initialPreviewAsData: true,
            initialPreview: this.initialPreviewData,
            initialPreviewConfig: this.initialPreviewConfigData
        });
      }
        /*
         $("#test-upload").on('fileloaded', function(event, file, previewId, index) {
         alert('i = ' + index + ', id = ' + previewId + ', file = ' + file.name);
         });
         */

}


/** 
Create instance of Admin code and also map the html elements to their handlers.

**/

$(document).ready(function () {

    url = "/cms/api/v2/cmsentries/" + view_json.id + "/";
    
    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            log.error("Failed to get cmscontent object from: ", url);
        },
        success: function(data){
            log.info("Created instance of Admin with cmsentry: ", data)
            var admin = new CategoryPageAdmin(data);
      
            $("#show-admin-overlay-button").click(function(){ admin.show();});
            $("#close-admin-overlay-button").click(function(){ admin.hide();});      
        }
    });
    
});




