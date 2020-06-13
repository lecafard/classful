import React, { useState, useEffect } from "react";
import "./App.scss";
import Select, { Option } from "./components/Select";
import { getTerms, getCourses, getCourse, postSubmission } from "./data/api";
import { CourseMap, CourseComponentMap } from "./data/responses";
import Input from "./components/Input";
import ReCAPTCHA from "react-google-recaptcha";

interface Notification {
  color?: string;
  message?: string;
  open: boolean;
}

const MAX_SECTIONS = 6;

// Default key is ReCaptcha test key
const RECAPTCHA_KEY = process.env.REACT_APP_RECAPTCHA_KEY || "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI";

function App() {
  const [coursesData, setCoursesData] = useState<CourseMap>({});
  const [termsData, setTermsData] = useState<Option[]>([]);
  const [componentData, setComponentData] = useState<CourseComponentMap>({});
  const [term, setTerm] = useState("");
  const [course, setCourse] = useState("");
  const [email, setEmail] = useState("");
  const [captcha, setCaptcha] = useState<string|null>("");
  const [selectedSections, setSelectedSections] = useState<string[]>([]);
  const [notification, setNotification] = useState<Notification>({
    color: "",
    message: "",
    open: false,
  });

  useEffect(() => {
    getTerms()
      .then(data => {
        setTermsData(data.data.sort().map((i: string) => ({value: i, text: i})));
      })
  }, []);

  useEffect(() => {
    if (term === "") {
      setCoursesData({});
      return setComponentData({});
    }
    getCourses(term)
      .then(data => {
        setCoursesData(data.data);
        if (!data.data[course]) {
          setCourse("");
        } else {
          loadComponents();
        }
      })
      .catch(data => {
        setNotification({
          color: "danger",
          message: data.error,
          open: true,
        });
      });
  }, [term]);

  useEffect(() => {
    if (course === "") return setComponentData({});
    loadComponents();
  }, [course]);

  function loadComponents() {
    getCourse(term, course)
      .then(data => {
        setComponentData(data.data.components);
      })
      .catch(data => {
        setNotification({
          color: "danger",
          message: data.error,
          open: true,
        });
      });
  }

  function submit(e: React.FormEvent) {
    e.preventDefault();

    if (!email || selectedSections.length === 0) return setNotification({
      message: "No classes selected.",
      color: "danger",
      open: true,
    });
    
    if (!captcha) return setNotification({
      message: "Please complete captcha",
      color: "danger",
      open: true,
    });

    postSubmission(captcha, email, selectedSections)
      .then(() => {
        setSelectedSections([]);
        setEmail("");
      }).catch(data => {
        setNotification({
          color: "danger",
          message: data.error,
          open: true,
        });
      });;
  }

  function handleSelection(section: string) {
    return () => {
      if (selectedSections.includes(section)) {
        setSelectedSections(selectedSections.filter(s => s !== section));
        return;
      }
      if (selectedSections.length === MAX_SECTIONS)
        return alert(`You are only allowed to select a maximum of ${MAX_SECTIONS} sections.`);
      setSelectedSections(selectedSections.concat(section));
    }
  }

  return (
    <div className="container" id="app">
      <p>
        Missed your perfect tute because it was taken by someone else? Classful will let
        you know when someone drops out of that class so that you can enrol!
      </p>
      {notification.open && <div className={`notification is-${notification.color}`}>
        {notification.message}
        <span className="delete" onClick={() => setNotification({open: false})}></span>
      </div>}
      <h2 className="title is-2 is-center">Selection</h2>
      <p>
        <b>Selected Sections: </b>
        {selectedSections.map((s) => (
          <span className="selected-session" onClick={handleSelection(s)}>{s}</span>
        ))}
      </p>
      <br />

      <Select
        options={termsData}
        defaultOption={{value: "", text: "Select Term"}}
        onChange={setTerm} 
      />
      <Select 
        options={Object.keys(coursesData).map((c) => ({
          value: c,
          text: `${c} - ${coursesData[c]}`
        }))}
        onChange={setCourse}
        defaultOption={{value: "", text: "Select Course"}}
      />
      <div>
        {Object.keys(componentData).length > 0 && <table className="table is-fullwidth" id="tbl-sections">
          <thead>
            <tr>
              <th>Code</th>
              <th>Type</th>
              <th>Status</th>
              <th>Capacity</th>
              <th>Times</th>
            </tr>
          </thead>
          <tbody>
            {Object.keys(componentData).sort().map(c => (
              <tr
                key={c}
                className={selectedSections.includes(`${term}_${course}_${c}`) ? "selected" : ""}
                onClick={handleSelection(`${term}_${course}_${c}`)}
              >
                <td>{c}</td>
                <td>{componentData[c].cmp_type}</td>
                <td>{componentData[c].status}</td>
                <td>{componentData[c].filled}/{componentData[c].maximum}</td>
                <td>{componentData[c].times}</td>
              </tr>
            ))}
          </tbody>
        </table>}
      </div>
      <br />

      <h2 className="title is-2 is-center">Notification</h2>
      <form onSubmit={submit}>
        <Input
          type="email"
          label="Email Address"
          value={email}
          placeholder="example@unsw.edu.au"
          onChange={setEmail}
          required={true}
        />
        <div style={{
          textAlign: "center"
        }}>
          <div className="recaptcha">
            <ReCAPTCHA
              sitekey={RECAPTCHA_KEY}
              onChange={setCaptcha}
              onExpired={() => setCaptcha("")}
            />
          </div>
        </div>
        <button className="button is-primary is-fullwidth is-large">Submit!</button>
      </form>
    </div>
  );
}

export default App;
