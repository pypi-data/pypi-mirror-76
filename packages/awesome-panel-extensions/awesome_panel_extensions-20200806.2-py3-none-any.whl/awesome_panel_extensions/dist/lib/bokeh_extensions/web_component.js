import { div, label } from "@bokehjs/core/dom";
import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import { bk_input_group } from "@bokehjs/styles/widgets/inputs";
function htmlDecode(input) {
    var doc = new DOMParser().parseFromString(input, "text/html");
    return doc.documentElement.textContent;
}
export class WebComponentView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.name.change, () => this.handleNameChange());
        this.connect(this.model.properties.innerHTML.change, () => this.render());
        this.connect(this.model.properties.attributesLastChange.change, () => this.handleAttributesLastChangeChange());
        this.connect(this.model.properties.propertiesLastChange.change, () => this.handlePropertiesLastChangeChange());
        this.connect(this.model.properties.columnDataSource.change, () => this.handleColumnDataSourceChange());
    }
    handleNameChange() {
        if (this.label_el)
            this.label_el.textContent = this.model.name;
    }
    render() {
        super.render();
        if (this.el.innerHTML !== this.model.innerHTML)
            this.createOrUpdateWebComponentElement();
    }
    after_layout() {
        if ("after_layout" in this.webComponentElement)
            this.webComponentElement.after_layout();
    }
    createOrUpdateWebComponentElement() {
        if (this.webComponentElement)
            this.webComponentElement.onchange = null;
        // @Philippfr: How do we make sure the component is automatically sized according to the
        // parameters of the WebComponent like width, height, sizing_mode etc?
        // Should we set height and width to 100% or similar?
        // For now I've set min_height as a part of .py __init__ for some of the Wired components?
        const title = this.model.name;
        if (this.model.componentType === "inputgroup" && title) {
            this.group_el = div({ class: bk_input_group }, this.label_el);
            this.group_el.innerHTML = htmlDecode(this.model.innerHTML);
            this.webComponentElement = this.group_el.firstElementChild;
            this.label_el = label({ style: { display: title.length == 0 ? "none" : "" } }, title);
            this.group_el.insertBefore(this.label_el, this.webComponentElement);
            this.el.appendChild(this.group_el);
        }
        else {
            this.el.innerHTML = htmlDecode(this.model.innerHTML);
            this.webComponentElement = this.el.firstElementChild;
        }
        this.activate_scripts(this.webComponentElement.parentNode);
        // Initialize properties
        this.initPropertyValues();
        this.handlePropertiesLastChangeChange();
        this.handleColumnDataSourceChange();
        // Subscribe to events
        this.webComponentElement.onchange = (ev) => this.handlePropertiesChange(ev);
        this.addEventListeners();
        this.addAttributesMutationObserver();
    }
    addAttributesMutationObserver() {
        if (!this.model.attributesToWatch)
            return;
        let options = {
            childList: false,
            attributes: true,
            characterData: false,
            subtree: false,
            attributeFilter: Object.keys(this.model.attributesToWatch),
            attributeOldValue: false,
            characterDataOldValue: false
        };
        const handleAttributesChange = (_) => {
            let attributesLastChange = new Object();
            for (let attribute in this.model.attributesToWatch) {
                const value = this.webComponentElement.getAttribute(attribute);
                attributesLastChange[attribute] = value;
            }
            if (this.model.attributesLastChange !== attributesLastChange)
                this.model.attributesLastChange = attributesLastChange;
        };
        let observer = new MutationObserver(handleAttributesChange);
        observer.observe(this.webComponentElement, options);
    }
    addEventListeners() {
        this.eventsCount = {};
        for (let event in this.model.eventsToWatch) {
            this.eventsCount[event] = 0;
            this.webComponentElement.addEventListener(event, (ev) => this.eventHandler(ev), false);
        }
    }
    transform_cds_to_records(cds) {
        const data = [];
        const columns = cds.columns();
        const cdsLength = cds.get_length();
        if (columns.length === 0 || cdsLength === null) {
            return [];
        }
        for (let i = 0; i < cdsLength; i++) {
            const item = {};
            for (const column of columns) {
                let array = cds.get_array(column);
                const shape = array[0].shape == null ? null : array[0].shape;
                if ((shape != null) && (shape.length > 1) && (typeof shape[0] == "number"))
                    item[column] = array.slice(i * shape[1], i * shape[1] + shape[1]);
                else
                    item[column] = array[i];
            }
            data.push(item);
        }
        return data;
    }
    // https://stackoverflow.com/questions/5999998/check-if-a-variable-is-of-function-type
    isFunction(functionToCheck) {
        if (functionToCheck) {
            const stringName = {}.toString.call(functionToCheck);
            return stringName === '[object Function]' || stringName === '[object AsyncFunction]';
        }
        else {
            return false;
        }
    }
    /**
     * Handles changes to `this.model.columnDataSource`
     * by
     * updating the data source of `this.webComponentElement`
     * using the function or property specifed in `this.model.columnDataSourceLoadFunction`
     */
    handleColumnDataSourceChange() {
        // @Philippfr: Right now we just reload all the data
        // For example Perspective has an `update` function to append data
        // Is this something we could/ should support?
        if (this.model.columnDataSource) {
            let data; // list
            const columnDataSourceOrient = this.model.columnDataSourceOrient;
            if (columnDataSourceOrient === "records")
                data = this.transform_cds_to_records(this.model.columnDataSource);
            else
                data = this.model.columnDataSource.data; // @ts-ignore
            const loadFunctionName = this.model.columnDataSourceLoadFunction.toString();
            const loadFunction = this.webComponentElement[loadFunctionName];
            if (this.isFunction(loadFunction))
                this.webComponentElement[loadFunctionName](data);
            else
                this.webComponentElement[loadFunctionName] = data;
        }
        // Todo: handle situation where this.model.columnDataSource is null
    }
    activate_scripts(el) {
        Array.from(el.querySelectorAll("script")).forEach((oldScript) => {
            const newScript = document.createElement("script");
            Array.from(oldScript.attributes)
                .forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            if (oldScript.parentNode)
                oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }
    // See https://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key
    /**
     * Example:
     *
     * `get_nested_property(element, "textInput.value")` returns `element.textInput.value`
     *
     * @param element
     * @param property_
     */
    get_nested_property(element, property_) {
        property_ = property_.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
        property_ = property_.replace(/^\./, ''); // strip a leading dot
        let a = property_.split('.');
        for (let i = 0, n = a.length; i < n; ++i) {
            let k = a[i];
            if (k in element)
                element = element[k];
            else
                return "";
        }
        return element;
    }
    set_nested_property(element, property_, value) {
        // @Phillipfr: I need your help to understand and solve this
        // hack: Setting the value of the WIRED-SLIDER before its ready
        // will destroy the setter.
        // I don't yet understand this.
        // if (["WIRED-SLIDER"].indexOf(element.tagName)>=0){
        //   const setter = element.__lookupSetter__(property_);
        //   if (!setter){return}
        // }
        const pList = property_.split('.');
        if (pList.length === 1)
            element[property_] = value;
        else {
            const len = pList.length;
            for (let i = 0; i < len - 1; i++) {
                const elem = pList[i];
                if (!element[elem])
                    element[elem] = {};
                element = element[elem];
            }
            element[pList[len - 1]] = value;
        }
    }
    /**
     * Handles events from `eventsToWatch` by
     *
     * - Incrementing the count of the event
     * - Checking if any properties have changed
     *
     * @param ev The Event Fired
     */
    eventHandler(ev) {
        let event = ev.type;
        this.eventsCount[event] += 1;
        let eventsCountLastChanged = {};
        eventsCountLastChanged[event] = this.eventsCount[event];
        this.model.eventsCountLastChange = eventsCountLastChanged;
        this.checkIfPropertiesChanged();
    }
    /** Checks if any properties have changed. In case this is communicated to the server.
     *
     * For example the Wired `DropDown` does not run the `onchange` event handler when the selection changes.
     * Insted the `select` event is fired. Thus we can subscribe to this event and manually check for property changes.
     */
    checkIfPropertiesChanged() {
        const propertiesChange = {};
        for (const property in this.model.propertiesToWatch) {
            const oldValue = this.propertyValues[property];
            const newValue = this.get_nested_property(this.webComponentElement, property);
            if (oldValue != newValue) {
                propertiesChange[property] = newValue;
                this.propertyValues[property] = newValue;
            }
        }
        if (Object.keys(propertiesChange).length)
            this.model.propertiesLastChange = propertiesChange;
    }
    /** Handles the `WebComponentElement` `(on)change` event
     *
     * Communicates any changed properties in `propertiesToWatch` to the server
     * by updating `this.model.propertiesLastChange`.
     * @param ev
     */
    handlePropertiesChange(ev) {
        const properties_change = new Object();
        for (const property in this.model.propertiesToWatch) {
            if (ev.detail && property in ev.detail) {
                properties_change[property] = ev.detail[property];
                this.propertyValues[property] = ev.detail[property];
            }
            else if (ev.target && property in ev.target) {
                properties_change[property] = ev.target[property];
                this.propertyValues[property] = ev.target[property];
            }
        }
        if (Object.keys(properties_change).length)
            this.model.propertiesLastChange = properties_change;
    }
    initPropertyValues() {
        this.propertyValues = new Object();
        if (!this.webComponentElement) {
            return;
        }
        for (let property in this.model.propertiesToWatch) {
            let old_value = this.propertyValues[property];
            let new_value = this.get_nested_property(this.webComponentElement, property);
            if (new_value !== old_value) {
                this.propertyValues[property] = new_value;
            }
        }
    }
    /**
     * Handles changes to `this.model.attributesLastChange`
     * by
     * updating the attributes of `this.webComponentElement` accordingly
     */
    handleAttributesLastChangeChange() {
        if (!this.webComponentElement)
            return;
        let attributesLastChange = this.model.attributesLastChange;
        for (let attribute in this.model.attributesLastChange) {
            if (attribute in this.model.attributesToWatch) {
                let old_value = this.webComponentElement.getAttribute(attribute);
                let new_value = attributesLastChange[attribute];
                if (old_value !== new_value) {
                    if (new_value === null)
                        this.webComponentElement.removeAttribute(attribute);
                    else
                        this.webComponentElement.setAttribute(attribute, new_value);
                }
            }
        }
    }
    /**
    * Handles changes to `this.model.propertiesLastChange`
    * by
    * updating the properties of `this.webComponentElement` accordingly
    */
    handlePropertiesLastChangeChange() {
        if (!this.webComponentElement) {
            return;
        }
        let propertiesLastChange = this.model.propertiesLastChange;
        for (let property in this.model.propertiesLastChange) {
            if (property in this.model.propertiesToWatch) {
                let value = propertiesLastChange[property];
                this.set_nested_property(this.webComponentElement, property, value);
            }
        }
    }
}
WebComponentView.__name__ = "WebComponentView";
export class WebComponent extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_WebComponent() {
        this.prototype.default_view = WebComponentView;
        this.define({
            // @Philipfr: How do I make property types more specific
            componentType: [p.String, 'htmlbox'],
            innerHTML: [p.String, ''],
            attributesToWatch: [p.Any],
            attributesLastChange: [p.Any],
            propertiesToWatch: [p.Any],
            propertiesLastChange: [p.Any],
            eventsToWatch: [p.Any],
            eventsCountLastChange: [p.Any],
            columnDataSource: [p.Any],
            columnDataSourceOrient: [p.Any],
            columnDataSourceLoadFunction: [p.Any],
        });
    }
}
WebComponent.__name__ = "WebComponent";
WebComponent.__module__ = "awesome_panel_extensions.bokeh_extensions.web_component";
WebComponent.init_WebComponent();
//# sourceMappingURL=web_component.js.map