// React component that will contain the Excalidraw math workspace.
import {Tldraw, useEditor, TldrawUiButton, toRichText, DefaultToolbar, DefaultToolbarContent} from 'tldraw'
import 'tldraw/tldraw.css'
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import { useState, useContext } from 'react';
import { Vision } from '../api';
import { chatProvider } from '../ChatHistoryManager.jsx';


export default function MathWhiteboard(){
    const [image, setImage] = useState("");
    const [AIOutput, setAIOutput] = useState("");
    const [loading, setLoading] = useState(false);
    const { history, write2History } = useContext(chatProvider);
    
    function ImageButton() {
        
        const editor = useEditor();
        
        
        
        
        return <TldrawUiButton
                    type="primary"
                    style={{ alignSelf: 'center', paddingLeft:'10px', paddingRight:'10px', color:'#459381'}}
                    onClick={async () => {
                        if (loading) return; 
                        setLoading(true); 

                        try{
                            const shapeIds = editor.getCurrentPageShapeIds();
                            if (shapeIds.size === 0) return alert('No shapes on the canvas')
                            const { blob } = await editor.toImage([...shapeIds], { format: 'png', background: true });
                            const response = await Vision(blob);
                            write2History(response);
                        }catch{
                            write2History("Failed to process message");
                        }finally{
                            setLoading(false);
                        }
                        
                        
                    }}>
                    <AutoAwesomeIcon/> Sumbit Work
                </TldrawUiButton>
    }

    function CustomToolbar() {
        return (
            <DefaultToolbar>
                <ImageButton/>
                <DefaultToolbarContent/>
            </DefaultToolbar>
        );
    }

    
    const allowedTools = new Set([
        'select',    // Cursor; also selects and moves shapes
        'hand',      // Drag to pan the canvas
        'draw',
        'arrow',
        'rectangle',
        'eraser',
        'ellipse',
        'line'
    ]);

    const overrides = {
        tools(_editor, tools) {
            return Object.fromEntries(
                Object.entries(tools).filter(([id]) => allowedTools.has(id))
            );
        },
    };

    return <div style={{ position: 'fixed', inset:0}}>
        <Tldraw overrides={overrides} components={{Toolbar:CustomToolbar}}/>
    </div>
}