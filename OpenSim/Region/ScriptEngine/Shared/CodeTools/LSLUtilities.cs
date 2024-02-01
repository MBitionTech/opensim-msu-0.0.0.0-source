///////////////////////////////////////////////////////////////////////////
//
// FILE NAME:      LSLUtilities.cs
//
// VERSION:        1.0
//
// AUTHOR:         Dr. Mel Bayne
//
// Date            Description
// --------        ----------------------------------------------------
// 01202024        This is a C# class of utility functions. It contains
//                 helper functions
//
///////////////////////////////////////////////////////////////////////////
using System;
using System.IO;
using System.Reflection;
using System.Text.RegularExpressions;
using log4net;

namespace SecondLife
{
    public class LSLUtilities
    {    
        private static readonly ILog m_log = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);
        public static readonly string m_PythonDLL = @".\python39.dll";

        public LSLUtilities() 
        {
            // Constructor
            //m_log.Debug("[LSLUtilities]:  constructor\n");
        }
        public void lsl_log(string name)
        {
            m_log.Debug(string.Format("[LSLUtilities]: lsl_log = {0}\n", name));
        }

        public string ProcessSpecialTags(string source)
        {
            Regex regex2 = new Regex(@"(XX_CREATEWORKDIR~(.*)_XX\s*\n)");
            Match match2 = regex2.Match(source);
            if (match2.Success)
            {
                // Get workingDirectory
                string workingDirectory = match2.Groups[2].Value;
                m_log.Debug("[LSLUtilities]: Found workingDirectory = '" + workingDirectory + "'.");

                // Replace any special tags as necessary
                source = source.Replace(match2.Groups[1].Value, "");
                source = source.Replace("XX_WORKDIR_XX", workingDirectory);

                // Create workingDirectory
                if (!Directory.Exists(workingDirectory))
                {
                    Directory.CreateDirectory(workingDirectory);
                }
            }
            else
            {
                m_log.Debug("[LSLUtilities]: No special tags found in Python source code.\n");
            }
            return source;
        }
    }
}

