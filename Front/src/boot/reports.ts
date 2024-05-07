import { userAuth } from './user-auth';

class Report {
  id: number | null;
  name: string;
  content: string;

  constructor(id: number | null, name: string, content: string) {
    this.id = id;
    this.name = name;
    this.content = content;
  }
}

class Reports {
  async saveReport(name: string, content: string) {
    console.log('Saving report ', name, content);
    return userAuth.post('/reports', {
      name: name,
      content: content,
    });
  }

  async getReports() {
    console.log('Getting reports');
    const response = await userAuth.get('/reports');
    return response.data.reports.map((report: any) => new Report(report.id, report.name, report.content));
  }
}

// TODO: is this not implemented in my version of quasar?
// export default boot(({ app }) => {
//   app.config.globalProperties.$reports = new Reports();
// });

const reports_api = new Reports();

export { reports_api, Report };
