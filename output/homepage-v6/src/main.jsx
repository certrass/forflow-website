import React from 'react';
import {createRoot} from 'react-dom/client';
import {App} from './App.jsx';
import {GovernancePage} from './GovernanceSection.jsx';
import './design-tokens.css';
import './showcase-viewport.css';
import './site-system.css';
import './product-system.css';
import './workspace-system.css';
import './capabilities-system.css';

createRoot(document.getElementById('root')).render(<React.StrictMode>{['/ai-governance','/ai-governance.html'].includes(location.pathname.replace(/\/$/,''))?<GovernancePage/>:<App/>}</React.StrictMode>);

import './product-films.css';
import './q2q-product.css';

import './showcase-stories.css';

import "./artifact-workspace.css";

import "./source-workbench.css";

import "./product-detail-refinements.css";

import "./human-details.css";

import "./product-editorial.css";

import "./motion-type.css";

import "./playback-refinements.css";

import './mainland-experience.css';
import './attio-fidelity.css';
import './lower-editorial.css';
import './governance.css';

import './connected-context.css';
import './method-motion.css';
import './evaluation-canvas.css';

import './narrative-refinements.css';

import "../public/assets/site/guru-navigation.css";
import './product-brand-alignment.css';
